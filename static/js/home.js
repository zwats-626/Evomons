document.getElementById("restart").addEventListener('click', () =>{
    create_form("restart");
})

document.getElementById("continue").addEventListener('click', () =>{
    create_form("continue")
})

function create_form(param){
    
    
    if (document.getElementById('delete-me')) return;

    const jumbo = document.getElementsByClassName("jumbotron")[0];
    const parent = document.createElement("div")
    parent.className = "mt-4";
    parent.id = "delete-me";
    jumbo.appendChild(parent);

    const form = document.createElement("form");
    form.action = "/";
    form.method = "get";
    form.className = "border rounded p-4 bg-light";
    parent.appendChild(form);

    const ste_container = document.createElement("div");
    ste_container.className = "form-continue";
    form.appendChild(ste_container);

    const input_elements = [
        {name: "steps", text: "Number of steps to simulate"},
        {name: "steps_length", text: "Number of turns in a step (a step is a recorded turn that is put into the database)"}
        
        
    ]
    console.log(param)
    let input_amt = param === "continue" ? 1: 2;
    console.log(input_amt)
    for(let i = 0; i < input_amt; i++){
        let in_name = input_elements[i].name;
        let un_text = input_elements[i].text;

        const wrapper = document.createElement("div");
        wrapper.className = "form-field mb-3";
        ste_container.appendChild(wrapper);

        const label = document.createElement('label');
        label.htmlFor = in_name;
        label.textContent = un_text;
        label.className = "form-label";
        wrapper.appendChild(label);

        const input = document.createElement('input');
        input.type = "number";
        input.name = in_name;
        input.id = in_name;
        input.className = "form-control";
        input.required = true;
        input.min = 1
        input.max = 1000
        wrapper.appendChild(input);
    }
    
    const sub_container = document.createElement('div');
    sub_container.className = "mt-3 text-end";
    form.appendChild(sub_container);

    const sub = document.createElement('input');
    sub.type = "submit";
    sub.value = param === "restart" ? "Restart" : "Continue";
    sub.className = "btn btn-primary";
    sub_container.appendChild(sub);
}