//const urlServer = 'http://localhost:8000' ; //Desarrollo
const urlServer = 'https://app-pasteleria-production.up.railway.app' ;
const restService = {

    get : async(url) => { 
        const response = await fetch(`${urlServer}/${url}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return await response.json();
    },

    post : async(params) => { 
        const response = await fetch(`${urlServer}/${params.url}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params.body)
        });
        return await response.json();
    },

    patch : async(params) => { 
        console.log("params");
        console.log(params)
        const response = await fetch(`${urlServer}/${params.url}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params.body)
        });
        return await response.json();
    },

}

const formMapper = {
    mapToForm : (keysName , data) => {
        keysName.map((val, indx )=>{
            document.getElementById(val).value = data[val];
        });
    },
    
    mapFormToJson : (formulario) => {
        const formData = new FormData(formulario);
        const datosJson = {};

        formData.forEach((valor, clave) => {
        datosJson[clave] = valor;
        });
        return datosJson;
    }
}