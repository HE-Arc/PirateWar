/**
 * Live display of available resource when filling the update ship form
 */
let default_values = {
    'crew': Number(document.getElementById('id_crew').value),
    'life': Number(document.getElementById('id_life').value),
    'cannons': Number(document.getElementById('id_cannon').value)
};

let default_player_resources_values = {
    'crew': Number(document.getElementById('player_crew').innerText),
    'cannons': Number(document.getElementById('player_cannons').innerText),
    'wood': Number(document.getElementById('player_wood').innerText),
};

document.getElementById('id_crew').min = 0;
document.getElementById('id_cannon').min = 0;
document.getElementById('id_life').min = 0;

function compute(default_player_resource_value, default_resource_value, current_value, factor, player_resource_element, input_id, resource_name) {
    try {
        //console.log(default_player_resource_value, default_resource_value, current_value, factor);
        if (default_player_resource_value + (default_resource_value - current_value) * factor >= 0) {
            default_player_resource_value += (default_resource_value - current_value) * factor;
            player_resource_element.innerText = '' + default_player_resource_value;
        }
        else {
            alert("Not enough resource");
            document.getElementById(input_id).value = default_resource_value;
        }
    }
    catch (err) {
        console.log(err);
    }
}

document.getElementById('id_crew').oninput = function (ev) {
    let current_value = Number(document.getElementById('id_crew').value);
    let default_player_resource_value = default_player_resources_values['crew'];
    let default_resource_value = default_values['crew'];
    let factor = 1;
    let player_resource_element = document.getElementById('player_crew');
    compute(default_player_resource_value, default_resource_value, current_value, factor, player_resource_element, 'id_crew');
};

document.getElementById('id_cannon').oninput = function (ev) {
    let currentValue = Number(document.getElementById('id_cannon').value);
    let default_player_resource_value = default_player_resources_values['cannons'];
    let default_resource_value = default_values['cannons'];
    let factor = 1;
    let player_resource_element = document.getElementById('player_cannons');
    compute(default_player_resource_value, default_resource_value, currentValue, factor, player_resource_element, 'id_cannon');
};

document.getElementById('id_life').oninput = function (ev) {
    let currentValue = Number(document.getElementById('id_life').value);
    let default_player_resource_value = default_player_resources_values['wood'];
    let default_resource_value = default_values['life'];
    let factor = 1;
    let player_resource_element = document.getElementById('player_wood');
    compute(default_player_resource_value, default_resource_value, currentValue, factor, player_resource_element, 'id_life');
};
