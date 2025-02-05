''' import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()

# Saturation and Phase Shift Pv Data (Pressure -> Specific Volume)
phase_change_data = {
    1: {"specific_volume_liquid": 0.001, "specific_volume_vapor": 1.694},
    5: {"specific_volume_liquid": 0.0012, "specific_volume_vapor": 0.374},
    10: {"specific_volume_liquid": 0.0035, "specific_volume_vapor": 0.0035},  # Critical Point
    15: {"specific_volume_liquid": 0.0015, "specific_volume_vapor": 0.141},
    20: {"specific_volume_liquid": 0.0017, "specific_volume_vapor": 0.057},
}

@app.get("/phase-change-diagram")
def get_phase_change(pressure: int = Query(..., description="Pressure in MPa")):
    """Returns specific volume for liquid and vapor at a given pressure."""
    if pressure in phase_change_data:
        return phase_change_data[pressure]
    return {"error": "Pressure value not found. Try values like 1, 5, 10, 15, or 20 MPa."}

# Run the FastAPI Server
if __name__ == "__main__":
    uvicorn.run("main_1:app", host="0.0.0.0", port=8000, reload=True) '''
    

import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()

def specific_volume_liquid(P):
    """Calculate specific volume of liquid using polynomial formula."""
    return round(((P-0.05)*((0.0035-0.00105)/(10-0.05)) + 0.00105),5)

def specific_volume_vapor(P):
    """Calculate specific volume of vapor using inverse power law."""
    return round(((P-0.05)*((0.0035-30)/(10-0.05))+30),5)



@app.get("/phase-change-diagram")
def get_phase_change(pressure: float = Query(..., description="Pressure in MPa")):
    """Returns calculated specific volumes for a given pressure."""
    
    # Define valid pressure range
    if not (0.05 <= pressure <= 20):
        return {"error": "Pressure out of range. Enter a value between 0.05 MPa and 20 MPa."}

    # Calculate volumes based on formula
    liquid_volume = specific_volume_liquid(pressure)
    vapor_volume = specific_volume_vapor(pressure)

    return {
        "specific_volume_liquid": liquid_volume,
        "specific_volume_vapor": vapor_volume
    }

# Run FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


    
    
