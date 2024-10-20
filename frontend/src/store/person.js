import axios from "axios";
import { url_utils, axios_api_cache } from "../utils/url_utils"

axios_api_cache.configure_axios(axios, true);
window.axios_api_cache = axios_api_cache;

export const person = {
    state: {
        newFaces: false,
        persons: [],
        allPersons: [],
        knownPersons: [],
        unknownFaces: [],
        recentFaces: [],
        mostRecentFaces: [],
        facesToConfirm: [],
        markMode: false,
        previewHeight: 100,
    },

    mutations: {
        setNewFaces(state, v) {
            state.newFaces = v;
        },

        setAllPersons(state, all) {
            state.allPersons = all;
        },
        setPersons(state, all) {
            state.persons = all;
        },
        setKnownPersons(state, known) {
            state.knownPersons = known;
        },
        setUnknownFaces(state, unknown) {
            state.unknownFaces = unknown;
        },
        setRecentFaces(state, recent) {
            state.recentFaces = recent;
        },
        setMostRecentFaces(state, recent) {
            state.mostRecentFaces = recent;
        },
        setFacesToConfirm(state, unknown) {
            state.facesToConfirm = unknown;
        },

        markMode(state, v) {
            state.markMode = v;
        },

        setPreviewHeight(state, v) {
            state.previewHeight = v;
        }
    },

    actions: {

        setRating(context, {photo, stars}) {
            let url = `/api/asset/setRating/${photo.id}/${stars}`;
            return new Promise((resolve => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            }))

        },

        ignoreFace(context, faceIds) {
            let url = '/api/face/ignore/';
            if (Array.isArray(faceIds)) {
                url += `${faceIds.join(",")}`
            } else if (faceIds.id) {
                    url += `${faceIds.id}`;
                } else {
                    url += `${faceIds}`;
                }           
            
            return new Promise((resolve => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            }))

        },
        resetFace(context, face) {
            let url = `/api/face/reset/${face.id}`;
            return new Promise((resolve => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            }))

        },
        getClosestPerson(context, face) {
            let url = `/api/face/nearestKnownFaces/${face.id}`
            return new Promise((resolve => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            }))

        },
        forgetPerson(context, person) {
            let url = `/api/person/forget/${person.id}`
            return new Promise((resolve => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            }))
        },

        ignoreUnknownPerson(context, person) {
            let url = `/api/person/ignore_unknown_person/${person.id}`
            return new Promise((resolve => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            }));
        },

        getAllUnknownFaces(context, {page, size, filters}) {
            let url = `/api/face/allUnknownAndClosest/${page}/${size}`;
            let args = "";
            if (filters) {
                args = url_utils.generateFilterArgs(filters);
            }
            url_utils.elementVisibility('.unknownFaces-loading', true);
            axios_api_cache.get(url+args).then( result => {
                context.commit("setUnknownFaces", result.data);    
            }).finally( () => {
                url_utils.elementVisibility('.unknownFaces-loading', false);
            });
        },

        getRecentFaces(context, {page, size, filters}) {
            url_utils.elementVisibility('.recentFaces-loading', true);
            let url = `/api/face/recent/${page}/${size}`;
            let args = "";
            if (filters) {
                args = url_utils.generateFilterArgs(filters);
            }
            axios_api_cache.get(url+args).then( result => {
                context.commit("setRecentFaces", result.data);    
            }).finally(  () => {
                url_utils.elementVisibility('.recentFaces-loading', false);
            })
            
        },

        getMostRecentFaces(context, {size}) {
            url_utils.elementVisibility('.mostRecentFaces-loading', true);
            let url = `/api/face/recent/1/${size}`;
            axios_api_cache.get(url).then( result => {
                context.commit("setMostRecentFaces", result.data);    
            }).finally( () => {
                url_utils.elementVisibility('.mostRecentFaces-loading', false);
            });
        },

        getFacesToConfirm(context, {page, size}) {
            let url = `/api/face/facesToConfirm/${page}/${size}`;
            url_utils.elementVisibility('.confirmFaces-loading', true);
            axios_api_cache.get(url).then( result => {
                context.commit("setFacesToConfirm", result.data);    
            }).finally( () => {
                url_utils.elementVisibility('.confirmFaces-loading', false);
            })
        },

        assignFaceToPerson(context, { person, name, faceId }) {
            let pid = null;
            if (person)
                pid = person.id;
            return new Promise((resolve => {
                axios.post("/api/face/assign_face_to_person", {
                    personId: pid,
                    name: name,
                    faceId: faceId,
                }).then( result => {
                    resolve(result.data);
                })
            }))

        },

        mergePerson(context, {src_person, target_person}) {
            let url = `/api/person/merge/${src_person.id}/${target_person.id}`;
            return new Promise((resolve) => {
                axios.get(url).then( result => {
                    resolve(result.data);
                })
            });

        },

        renamePerson(context, {person, name}) {
            return new Promise((resolve) => {
                axios.post("/api/person/rename", {
                    personId: person.id,
                    name: name
                }).then( result => {
                    resolve(result.data);
                })
            });

        },
        /*
        getKnownPersons() {
            return new Promise((resolve => {
                axios.get("/api/person/known").then (result => {
                    resolve(result.data)
                })
            }))
        },
        */
        getKnownPersons(context) {
            axios_api_cache.get("/api/person/known").then (result => {
                context.commit("setKnownPersons", result.data);    
            });
        },

        getAllPersons(context) {
            axios_api_cache.get("/api/person/all").then (result => {
                context.commit("setAllPersons", result.data);
            });
        },

        getPersons(context, {page, size, filters}) {
            url_utils.elementVisibility('.persons-loading', true);
            let url = `/api/person/${page}/${size}`;
            let args = "";
            if (filters) {
                args = url_utils.generateFilterArgs(filters);
            }
            url_utils.elementVisibility('.persons-loading', true);
            axios_api_cache.get(url+args).then( result => {
                context.commit("setPersons", result.data);
            }).finally( () => {
                url_utils.elementVisibility('.persons-loading', false);
            })
        },

        getPersonsByPhoto(context, photo) {
            return new Promise((resolve => {
                axios.get("/api/person/by_asset/" + photo.id).then((result) =>{
                    resolve(result.data);
                })
            }))
        },
        getFacesByPhoto(context, photo) {
            return new Promise((resolve => {
                axios.get("/api/face/by_asset/" + photo.id).then((result) =>{
                    resolve(result.data);
                })
            }))
        },
        getExifForPhoto(context, photo) {
            return new Promise((resolve => {
                axios.get("/api/asset/exif/" + photo.id).then((result) =>{
                    resolve(result.data);
                })
            }))
        },

        getGpsForPhoto(context, photo) {
            return new Promise((resolve => {
                axios.get("/api/asset/gps/" + photo.id).then((result) =>{
                    resolve(result.data);
                })
            }))
        },

        getThingsForPhoto(context, photo) {
            return new Promise((resolve => {
                axios.get("/api/asset/things/" + photo.id).then((result) =>{
                    resolve(result.data);
                })
            }))
        },

        getAssetDuplicates(context, photo) {
            return new Promise((resolve => {
                axios.get("/api/asset/duplicates/" + photo.checksum).then((result) =>{
                    resolve(result.data);
                })
            }))
        },

        getAllTags() { //context
            return new Promise((resolve => {
                axios.get("/api/tags").then((result) =>{
                    resolve(result.data);
                })
            }))
        },
        removeTagsFromAsset(context, { assetId, tagNames }) {
            return new Promise((resolve => {
                axios.delete(`/api/asset/tags/${assetId}/${tagNames}`).then((result) =>{
                    resolve(result.data);
                });
            }));
        },
        setAssetTags(context, { assetId, tagNames }) {
            let url = `/api/asset/tags/${assetId}/`;
            if (Array.isArray(tagNames)) {
                url += `${tagNames.join(",")}`
            } else {
                url += `${tagNames}`;
            }           
            return new Promise((resolve => {
                axios.put(url).then((result) =>{
                    resolve(result.data);
                });
            }));
        },
        
        getUnknownFaces(context, index) {
            return new Promise((resolve => {

                axios.get("/api/cluster/faces/" + index).then((result) => {
                    resolve(result.data);
                })
            }))
        },

        updateAllFacesIdentified(context, {photo, facesAllIdentified}) {
            let url = `/api/asset/setFacesAllIdentified/${photo.id}/${facesAllIdentified}`;
            axios_api_cache.get(url).then( result => {
              console.log(`Marking ${photo.id} as all faces identified = ${facesAllIdentified} with result`, result)
            })
        },

    }
}
  