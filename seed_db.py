from sqlmodel import Session, select
from app.db import engine, init_db
from app.models import Experiment, Condition

def seed():
    init_db()
    with Session(engine) as session:
        # Check if experiment exists
        exp = session.exec(select(Experiment).where(Experiment.name == "default")).first()
        if not exp:
            exp = Experiment(name="default", description="Default experiment")
            session.add(exp)
            session.commit()
            print("Created default Experiment")
        session.refresh(exp)

        # Check if condition exists
        cond = session.exec(select(Condition).where(Condition.experiment_id == exp.id)).first()
        if not cond:
            cond = Condition(
                experiment_id=exp.id,
                name="control", # Use lowercase as convention
                system_prompt="You are a helpful assistant.",
                llm_model="llama3.2:latest",
                is_active=True
            )
            session.add(cond)
            session.commit()
            print("Created Control Condition")
        
        print(f"Seeding Complete. Experiment ID: {exp.id}")

if __name__ == "__main__":
    seed()
