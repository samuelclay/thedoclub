window.DC = {};

DC.PresentationEditor = function(options) {
    this.options = options || {};
    this.$el = this.options.$el;
    
    this.initialize();
};

DC.PresentationEditor.prototype = {
    
    initialize: function() {
        $("textarea", this.$el).bind('keyup', _.bind(this.renderPreview, this));
        this.renderPreview();
    },
    
    renderPreview: function() {
        var slideHtml = this.slideHtml();
        $(".preview", this.$el).html(slideHtml);
    },
    
    slideHtml: function() {
        var text = $("textarea", this.$el).val();
        return marked.parse(text);
    }
    
};

$(document).ready(function() {

    $('.slide').each(function() {
        new DC.PresentationEditor({
            '$el': $(this)
        });
    });

});