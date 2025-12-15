from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from flask import Flask, render_template, make_response, request
from . import create_new_eco, run_sim, get_dem, get_biomass
import json
import sqlalchemy
from sqlalchemy import JSON
from sqlalchemy import LargeBinary
import pickle, os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

app = Flask(__name__, 
            template_folder=os.path.join(PROJECT_ROOT, 'templates'),
            static_folder=os.path.join(PROJECT_ROOT, 'static'))
db_path = db_path = os.path.join("instance", "enviroment.db")
db = sqlalchemy.create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=db)
Base = declarative_base()

STEPS = 0
STEPS_LENGTH = 5 

class Turn(Base):
    __tablename__ = "turns"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    turn_number: Mapped[int] = mapped_column(unique=True)
    Mon_Count: Mapped[int] = mapped_column()
    Plant_Count: Mapped[int] = mapped_column()
    Remains_Count: Mapped[int] = mapped_column()
    Mon_Biomass: Mapped[int] = mapped_column()
    Plant_Biomass: Mapped[int] = mapped_column()
    Remains_Biomass: Mapped[int] = mapped_column()
    Step_Leng: Mapped[int] = mapped_column()
    
    eco_pickle: Mapped[bytes] = mapped_column(LargeBinary)

    def __repr__(self):
        return f"<Turn(id={self.id}, turn={self.turn_number})>"
    
    @property
    def eco(self):
        return pickle.loads(self.eco_pickle)
    
    @eco.setter
    def eco(self, value):
        self.eco_pickle = pickle.dumps(value)

Base.metadata.create_all(db)

def main() -> None:
    with Session() as session:
        if not session.query(Turn).first():
            cold_open()

@app.route('/', methods=['GET'])
def load_homepage():
    global STEPS, STEPS_LENGTH
    steps_lg = request.args.get('steps_length')
    steps = request.args.get('steps')
    
    if steps and not steps_lg:
        STEPS = int(steps)
        print(steps)
        continue_sim()
    elif steps and steps_lg:
        STEPS, STEPS_LENGTH = int(steps), int(steps_lg)
        with Session() as session:
            session.query(Turn).delete()
            session.commit()
        cold_open()
        continue_sim()
    return render_template('home.html')

@app.route('/inspector')
def eco_index():
    turn = get_recent_turn()
    return render_template("inspector.html", turn=turn.turn_number)

@app.route('/api/eco', methods=['GET'])
def get_eco():
    flag = request.args.get('turn')
    current_turn_num = request.args.get('current', type=int)

    if current_turn_num is not None:
        with Session() as session:
            current_turn = session.query(Turn).filter_by(turn_number=current_turn_num).first()
            if current_turn:
                session.expunge(current_turn)
    else:
        current_turn = get_recent_turn()

    if flag and current_turn:
        turn = toggle_turns(flag, current_turn)
    else:
        turn = current_turn if current_turn else get_recent_turn()

    # Convert pickled eco objects to JSON-serializable dicts
    eco_dicts = [obj.to_dict() for obj in turn.eco]
    
    response_data = {
        'eco': eco_dicts,
        'turn_number': turn.turn_number
    }
    
    response = make_response(json.dumps(response_data, sort_keys=False))
    response.headers['Content-Type'] = 'application/json'
    return response
    
@app.route('/organizer')
def eco_grapher():
    return render_template("organizer.html")

@app.route('/api/graph', methods=['GET'])
def get_graph():
    flags = request.args.getlist('target')
    
    color = None
    cohort = "Unknown"
    data_type = "Unknown"

    try:
        color, cohort, data_type = flags[0], flags[1], flags[2]
        graph_data = []
        data_type = "Count" if data_type == "Population" else data_type
        attr_name = f"{cohort}_{data_type}"
        with Session() as session:
            turns = session.query(Turn).order_by(Turn.turn_number.asc()).all()
            graph_data = [getattr(turn, attr_name, 0) for turn in turns]
            max_val = max(graph_data) if graph_data else 0

            """
               for turn in turns:
                
                val = 0
                if cohort == "Mon":
                    if data_type == "Population":
                        val = turn.Mon_Count
                    elif data_type == "Biomass":
                        val = turn.Mon_Biomass
                elif cohort == "Plant":
                    if data_type == "Population":
                        val = turn.Plant_Count
                    elif data_type == "Biomass":
                        val = turn.Plant_Biomass
                elif cohort == "Remains":
                    if data_type == "Population":
                        val = turn.Remains_Count
                    elif data_type == "Biomass":
                        val = turn.Remains_Biomass
                else:
                    raise ValueError(f"Unknown cohort: {cohort}")
                
                if val > max_val:
                    max_val = val
                graph_data.append(val)
                
            
            """
         

        response_data = {
            'graph_data': graph_data,
            'max_cord': max_val,
            'ordinate': f"{cohort} {data_type}",
            'color': color
        }

        response = make_response(json.dumps(response_data, sort_keys=False))
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        # Log the full error
        import traceback
        print("ERROR in get_graph:")
        print(traceback.format_exc())
        
        # Return JSON error instead of HTML
        error_response = {
            'error': str(e),
            'graph_data': [],
            'ordinate': f"{cohort} {data_type}"
        }
        response = make_response(json.dumps(error_response), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
 
def cold_open(): 
    eco = create_new_eco()
    turn = Turn(turn_number=0)
    turn.eco = eco  
    turn.Mon_Count, turn.Plant_Count, turn.Remains_Count = get_dem(eco)
    turn.Mon_Biomass, turn.Plant_Biomass, turn.Remains_Biomass = get_biomass(eco) 
    turn.Step_Leng = STEPS_LENGTH
    print(f"in cold open turn mon count is {turn.Mon_Count}")
    with Session() as session:
         session.add(turn)
         session.commit()

def continue_sim():
    for _ in range(STEPS):
        print(f"steps: {STEPS}")
        print("in continue")
        turn = get_recent_turn()
        if turn.Mon_Count <= 0:
            print("in break")
            break
        print("past break")
        eco = turn.eco
        sl = turn.Step_Leng
        eco, new_turn_num = run_sim(eco, turn.turn_number, sl)
        next_turn = Turn(turn_number=new_turn_num)
        next_turn.eco = eco
        next_turn.Step_Leng = sl
        next_turn.Mon_Count, next_turn.Plant_Count, next_turn.Remains_Count = get_dem(eco)
        next_turn.Mon_Biomass, next_turn.Plant_Biomass, next_turn.Remains_Biomass = get_biomass(eco) 
        
        with Session() as session:
            session.add(next_turn)
            session.commit()
        
def get_recent_turn():
    with Session() as session:
        turn = session.query(Turn).order_by(Turn.turn_number.desc()).first()
        if turn:
            session.expunge(turn)
        return turn
    
def toggle_turns(flag, current_turn: Turn) -> Turn:
    with Session() as session:
        if flag == "next":
            print("next button")
            
            # Reattach current_turn to this session
            current_turn = session.merge(current_turn)
            
            # Get the most recent turn in this session
            recent_turn = session.query(Turn).order_by(Turn.turn_number.desc()).first()
            
            if current_turn.turn_number >= recent_turn.turn_number:
                print("already at most recent turn")
                return current_turn
            
            turn = (
                session.query(Turn)
                .filter(Turn.turn_number > current_turn.turn_number)
                .order_by(Turn.turn_number.asc())
                .first()
            )
        elif flag == "back":
            print("back button")
            turn = (
                session.query(Turn)
                .filter(Turn.turn_number < current_turn.turn_number)
                .order_by(Turn.turn_number.desc())
                .first()
            )
        else:
            turn = current_turn
        
        # If turn is None, return current_turn
        if turn is None:
            return current_turn
            
        # Expunge to keep the object accessible after session closes
        session.expunge(turn)
        return turn

if __name__ == '__main__':
    main()
    app.run(debug=True)