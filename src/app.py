"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports-related activities (added)
    "Soccer Team": {
        "description": "Competitive soccer practices and matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap swimming, technique coaching, and meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    # Artistic activities (added)
    "Art Club": {
        "description": "Painting, drawing, and mixed-media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater workshops, rehearsals, and productions",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    # Intellectual activities (added)
    "Debate Team": {
        "description": "Practice public speaking, argumentation, and competitions",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["elijah@mergington.edu", "logan@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design and build robots for challenges and competitions",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["zachary@mergington.edu", "natalie@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)

    # Validate student is not already signed up
    if activity["participants"].count(email) > 1:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    


    return {"message": f"Signed up {email} for {activity_name}"}


# Nieuwe endpoint om een deelnemer te verwijderen
from fastapi import Query
@app.delete("/activities/{activity_name}/unregister")
def unregister_participant(activity_name: str, email: str = Query(...)):
    """Verwijder een deelnemer uit een activiteit"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    activity["participants"].remove(email)
    return {"message": f"{email} is verwijderd uit {activity_name}"}
