async function loadStates() {
    let res = await fetch('/states');
    let result = await res.json();
    let data = result.data;

    let state = document.getElementById("state");
    state.innerHTML = "";

    data.forEach(s => {
        let opt = document.createElement("option");
        opt.value = s;
        opt.text = s;
        state.appendChild(opt);
    });

    loadDistricts();
}

async function loadDistricts() {
    let stateVal = document.getElementById("state").value;

    let res = await fetch(`/districts?state=${encodeURIComponent(stateVal)}`);
    let result = await res.json();
    let data = result.data;

    let district = document.getElementById("district");
    district.innerHTML = "";

    data.forEach(d => {
        let opt = document.createElement("option");
        opt.value = d;
        opt.text = d;
        district.appendChild(opt);
    });

    loadSubdistricts();
}

async function loadSubdistricts() {
    let districtVal = document.getElementById("district").value;

    let res = await fetch(`/subdistricts?district=${encodeURIComponent(districtVal)}`);
    let result = await res.json();
    let data = result.data;

    let sub = document.getElementById("subdistrict");
    sub.innerHTML = "";

    data.forEach(s => {
        let opt = document.createElement("option");
        opt.value = s;
        opt.text = s;
        sub.appendChild(opt);
    });

    loadVillages();
}

async function loadVillages() {
    let subVal = document.getElementById("subdistrict").value;

    let res = await fetch(`/villages?subdistrict=${encodeURIComponent(subVal)}`);
    let result = await res.json();
    let data = result.data;

    let list = document.getElementById("villages");
    list.innerHTML = "";

    data.forEach(v => {
        let li = document.createElement("li");
        li.innerText = v;
        list.appendChild(li);
    });
}

// events
document.getElementById("state").onchange = loadDistricts;
document.getElementById("district").onchange = loadSubdistricts;
document.getElementById("subdistrict").onchange = loadVillages;

// start
window.onload = loadStates;