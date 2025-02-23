import requests

OPENFDA_API_URL = "https://api.fda.gov/drug/event.json"

def get_adverse_events(drug1, drug2):
    """
    Query the OpenFDA API for adverse event reports involving both drugs
    and filter events caused by the combination.
    """
    try:
        query = f'"{drug1}" AND "{drug2}"'
        response = requests.get(
            OPENFDA_API_URL,
            params={"search": f"patient.drug.medicinalproduct:{query}", "limit": 100}
        )
        if response.status_code == 200:
            data = response.json()
            results = []

            # Parse and filter events
            for event in data.get("results", []):
                drugs_in_event = event.get("patient", {}).get("drug", [])
                # Extract drugs marked as "suspect" in the report
                suspect_drugs = [
                    drug.get("medicinalproduct", "").lower()
                    for drug in drugs_in_event
                    if drug.get("drugcharacterization", "") == "1"  # "1" means suspect
                ]

                # Ensure both drugs are marked as suspect
                if drug1.lower() in suspect_drugs and drug2.lower() in suspect_drugs:
                    results.append({
                        "reaction": event.get("patient", {}).get("reaction", [{}])[0].get("reactionmeddrapt", "N/A"),
                        "description": event.get("safetyreportid", "No description available"),
                    })

            return results
        else:
            return {"error": f"OpenFDA API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
