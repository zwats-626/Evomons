let currentTurnNumber = window.INITIAL_TURN;

async function current_eco(flag = "null") {
    const url = flag
        ? `/api/eco?turn=${flag}&current=${currentTurnNumber}` 
        : '/api/eco';
    const response = await fetch(url);
    const data = await response.json();
    console.log("Eco data:", data);

    // Update current turn number and display
    currentTurnNumber = data.turn_number;
    document.getElementById('turn-display').textContent = `Turn: ${data.turn_number}`;
    
    // Regenerate sidebar buttons for new eco data
    updateEcoButtons(data.eco);
    
    // Load first object
    load_obj(data.eco[0]);
}

function updateEcoButtons(eco) {
    const container = document.getElementById('eco-buttons');
    container.innerHTML = ''; // Clear existing buttons
    
    eco.forEach((obj, index) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-primary btn-dark';
        btn.setAttribute('data-bs-toggle', 'button');
        btn.id = `eco-btn-${index}`;
        let s = '' 
        if (obj.type == 'mon'){
            s = obj.species
        }
        btn.textContent = obj.type + s;
        
        btn.addEventListener('click', () => {
            load_obj(obj);
        });
        
        container.appendChild(btn);
    });
}

window.onload = current_eco('next');

document.getElementById('back').addEventListener('click', () => {
    current_eco("back");
})
document.getElementById('next').addEventListener('click', () => {
    current_eco("next");
})

function load_obj(obj) {
    document.getElementById("lv-exp").innerHTML = `Level: ${obj.level} Exp: ${obj.exp}`;
    let traits_html = ""
    
    traits_html += "<tr><td>Trait</td>";
    for (let trait in obj.traits){
        traits_html += `
        <td>
            ${trait} 
        </td>
        `
    }
    traits_html += "</tr><td>Power</td>"
    for (let trait in obj.traits){
        traits_html += `
        <td>
            ${obj.traits[trait]} 
        </td>
        `
    }
    traits_html += "</tr>"


    document.getElementById("traits-table").innerHTML = traits_html;


    let stats_html = `
    <tr>
        <td></td>
        <td> Level </td>
    `
    for (let stat in obj.stats){
        stats_html +=`
            <td> ${stat} </td>    
        `
    }
    stats_html += `<td> Energy </td>       
        </tr>
        `
    for (let [statObj, label, lvl, size] of [
        [obj.stats, "base stats", 100, obj.size],
        [obj.max_stats, "max stats", obj.max_level, obj.max_size],
        [obj.current_stats, "current stats", obj.level, obj.current_size]]) {                
        stats_html +=   `
            <tr>
            <td> ${label} </td>
            <td> ${lvl} </td>
            `
        for (let stat in statObj){
            if (statObj == obj.current_stats){
                stats_html += `<td> ${statObj[stat]} (${(statObj[stat] - obj.buffs[stat])}) </td>`;
            }
            else{
                stats_html += `<td> ${statObj[stat]} </td>`
            }
        }
        if (statObj != obj.current_stats){
            stats_html += `<td> ${size} </td> </tr>`;
        }
        else{
            stats_html += `<td> ${size} (${size - obj.energy})</td> </tr>`;
        }
    }
    document.getElementById("stats-table").innerHTML = stats_html;


    if (obj.type != 'mon'){
        document.getElementById("moves-table").innerHTML = '';
        document.getElementById("move-h").innerHTML = '';
        document.getElementById("brain").innerHTML = ''
        
        for (const canv of [document.getElementById("basic-display"),
        document.getElementById("encounter-display")])
            if (canv) {
                canv.style.border = "none";
                const ctx = canv.getContext("2d");
                ctx.clearRect(0, 0, canv.width, canv.height);
            }
        return
    }
    moves_html = `<tr>
        <td></td>
        <td>Level</td>
        `
    moves = {...obj.basic_moves, ...obj.encounter_moves }
    for (let move in moves){
        moves_html += `<td>${move}</td>`
    }
    moves_html += "</tr>"; 
    for (let [movesObj, label, lvl] of [
        [moves, "base moves", 100],
        [obj.max_moves, "max moves", obj.max_level],
        [obj.current_moves, "current moves", obj.level],
    ]) {
        
        moves_html += `
            <tr>
            <td>${label}</td>
            <td>${lvl}</td>
        `
        for (let move in movesObj){
            moves_html += `<td>${movesObj[move]}</td>`;
        }
        moves_html += `</tr>`;
    }

    
    document.getElementById("moves-table").innerHTML = moves_html;
    document.getElementById("move-h").innerHTML = 'Moves';

    render_brain(obj);
    
}

function render_brain(obj) {
    document.getElementById("brain").innerHTML = 'Brain'

    for (let [brain, display_id] of [[obj.brain.basic, "basic-display"], 
                                    [obj.brain.encounter, "encounter-display"]]){
        const canvas = document.getElementById(display_id);
        const maxNum = Math.max(brain.inputs.length, 
                                brain.hiddens.length, 
                                brain.outputs.length);
        height = maxNum * 100
        canvas.height = height + 25
        canvas.width = 3 * 200
        canvas.style.border = "1px solid black";
        const ctx = canvas.getContext("2d");

        x = 50;
        for (let [layer, next_layer] of [[brain.inputs, brain.hiddens.length], 
                        [brain.hiddens, brain.outputs.length], 
                        [brain.outputs, 0]]){
            y = 50;
            for(let i = 0; i < layer.length; i++){
                
                let neuron = layer[i];
                for (let j = 0; j < neuron.axons.length; j++){
                    axon = neuron.axons[j];
                    if  (axon < next_layer){
                        ctx.beginPath();       
                        ctx.moveTo(x, y);      
                        ctx.lineTo((x + 200), (100 * axon + 50));     
                        ctx.stroke();             
                    }
                }

                ctx.fillStyle = "black";            
                ctx.font = "10px Arial";            
                ctx.textAlign = "center";           
                ctx.textBaseline = "middle";        
                ctx.fillText(neuron.action, x, y + 50);

                ctx.beginPath();
                ctx.arc(x, y, 25, 0, Math.PI * 2); 
                ctx.fillStyle = "green";
                ctx.fill();   
                ctx.stroke(); 
                
                y += 100;
            }
            x += 200
        }
    } 
}