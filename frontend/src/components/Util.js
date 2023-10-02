

export function isElementInViewport (el) {
    let rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}

/**
 * fullVisible=true only returns true if the all object rect is visible
 */
export function isReallyVisible(el, fullVisible, offset=0, prevRect=null) {
    if ( el.tagName == "HTML" )
            return true;
    let parentRect = el.parentNode.getBoundingClientRect();
    let rect = prevRect || el.getBoundingClientRect();
    let result = (
            ( fullVisible ? rect.top    >= parentRect.top    : rect.bottom - offset > parentRect.top ) &&
            ( fullVisible ? rect.left   >= parentRect.left   : rect.right  > parentRect.left ) &&
            ( fullVisible ? rect.bottom <= parentRect.bottom : rect.top  < parentRect.bottom ) &&
            ( fullVisible ? rect.right  <= parentRect.right  : rect.left   < parentRect.right ) &&
            isReallyVisible(el.parentNode, false, offset, rect)
    )
    return result;
}

export function isVisible(el, percentX = 100, percentY=100){
    var tolerance = 0.01;   //needed because the rects returned by getBoundingClientRect provide the position up to 10 decimals

    var elementRect = el.getBoundingClientRect();
    var parentRects = [];
    var element = el;

    while(element.parentElement != null){
        parentRects.push(element.parentElement.getBoundingClientRect());
        element = element.parentElement;
    }

    var visibleInAllParents = parentRects.every(function(parentRect){
        var visiblePixelX = Math.min(elementRect.right, parentRect.right) - Math.max(elementRect.left, parentRect.left);
        var visiblePixelY = Math.min(elementRect.bottom, parentRect.bottom) - Math.max(elementRect.top, parentRect.top);
        var visiblePercentageX = visiblePixelX / elementRect.width * 100;
        var visiblePercentageY = visiblePixelY / elementRect.height * 100;
        return visiblePercentageX + tolerance > percentX && visiblePercentageY + tolerance > percentY;
    });
    return visibleInAllParents;
}

export function setActionOnFace(faceId, action, rootElement) {
    let elementCss = `${rootElement}[face_id='${faceId}']`; 
    let elements = document.querySelectorAll(elementCss);
    for(let faceIndex = 0; faceIndex < elements.length; faceIndex++) {
        let element = elements[faceIndex];
        let plateElement = elements[faceIndex].parentElement;
        switch (action) {
            case "running": {
                plateElement.style.border = "1px solid red";
                break;
            }
            case "delete": {
                plateElement.style.display = "none";
                plateElement.style.border = "1px solid gray";
                break;
            }
            case "hide": {
                plateElement.style.visibility = "hidden";
                break;
            }
            case "highlight": {
                element.style.backgroundColor = "#D0D0D0";
                break;
            }
            case "unhighlight": {
                element.style.backgroundColor = "transparent";
                break;
            }
            default: {
                console.log(`Unknown action '${action}' requested on face ${faceId}.`)
            }
        }
    }
}

export function setActionOnPerson(personId, action, rootElement) {
    let elementCss = `${rootElement}[person_id='${personId}']`; 
    let elements = document.querySelectorAll(elementCss);
    for(let personIndex = 0; personIndex < elements.length; personIndex++) {
        let element = elements[personIndex];
        let plateElement = elements[personIndex].parentElement;
        switch (action) {
            case "running": {
                plateElement.style.border = "1px solid red";
                break;
            }
            case "delete": {
                plateElement.style.display = "none";
                plateElement.style.border = "1px solid gray";
                break;
            }
            case "hide": {
                plateElement.style.visibility = "hidden";
                break;
            }
            case "highlight": {
                element.style.backgroundColor = "#D0D0D0";
                break;
            }
            case "unhighlight": {
                element.style.backgroundColor = "transparent";
                break;
            }
            default: {
                console.log(`Unknown action '${action}' requested on person ${personId}.`)
            }
        }
    }
}
