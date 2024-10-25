from fastapi import HTTPException
from datetime import timedelta

# Etapas del ciclo vegetativo
CYCLE_STAGES = {
    "emergence": 10,
    "tillering": 20,
    "panicleInitiation": 30,
    "flowering": 40,
    "ripening": 50
}

def generateCropCycle(sowingDate):
    try:
        stages = []
        currentDate = sowingDate

        for stage, days in CYCLE_STAGES.items():
            stageEnd = currentDate + timedelta(days=days)
            stages.append({
                "stage": stage,
                "startDate": currentDate,
                "endDate": stageEnd
            })
            currentDate = stageEnd

        return stages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating crop cycle: {str(e)}")
