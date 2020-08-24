//Add an API class which helps to call the API
const getJSON = (path, options) =>
    fetch(path, options)
        .then(res => res.json())
class API {
    constructor(url = 'http://localhost:5000') {
        this.url = url;
    }
    apiRequest(path, options) {
        return getJSON(`${this.url}/${path}`, options);
    }
}
export default API;