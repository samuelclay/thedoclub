window.DC = {};

DC.Homepage = function() {
    console.log(["Homepage"]);
};

$(document).ready(function() {

    DC.homepage = new DC.Homepage();

});