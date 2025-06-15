import pandas as pd

class ReportGenerator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def outstanding_billables(self):
        data = pd.DataFrame(self.db_manager.fetch_all_records())
        if data.empty:
            return {"Total Outstanding Billables": "$0.00"}
        data["Outstanding"] = data["AmountBilled"].astype(float) - data["AmountPaid"].astype(float)
        return {"Total Outstanding Billables": f"${data['Outstanding'].sum():.2f}"}

    def unpaid_patients(self):
        data = pd.DataFrame(self.db_manager.fetch_all_records())
        if data.empty:
            return []
        data["Outstanding"] = data["AmountBilled"].astype(float) - data["AmountPaid"].astype(float)
        unpaid = data[data["Outstanding"] > 0][["PatientName", "Outstanding"]]
        return unpaid.to_dict(orient="records")

    def revenue_per_month(self):
        data = pd.DataFrame(self.db_manager.fetch_all_records())
        if data.empty:
            return []
        data["DateOfVisit"] = pd.to_datetime(data["DateOfVisit"])
        report = data.groupby(data["DateOfVisit"].dt.strftime('%Y-%m'))["AmountPaid"].sum().reset_index()
        return report.to_dict(orient="records")

    def top_insurance_providers(self):
        data = pd.DataFrame(self.db_manager.fetch_all_records())
        if data.empty:
            return []
        report = data.groupby("Insurance")["AmountPaid"].sum().reset_index().sort_values(by="AmountPaid", ascending=False)
        return report.to_dict(orient="records")
