window.DC = {};

DC.PresentationEditor = function(options) {
    this.options = options || {};
    this.$el = this.options.$el;
    
    console.log(["PresentationEditor", options, this.$el]);
    this.initialize();
};

DC.PresentationEditor.prototype = {
    
    initialize: function() {
        this.autosave();
        this.renderPreview({skip_save: true});
        $("textarea", this.$el).bind('keyup', _.bind(this.renderPreview, this, {}));
    },
    
    renderPreview: function(options) {
        options = options || {};
        console.log(["renderPreview", options]);
        var slideHtml = this.slideHtml(this.$el);
        $(".slide-preview", this.$el).html(slideHtml);
        if (!options.skip_save) {
            this._throttleSave();
            this._debounceSave();
        }
    },
    
    slideText: function($el) {
        return $("textarea", $el).val();
    },
    
    slideHtml: function($el) {
        var text = this.slideText($el);
        return marked.parse(text);
    },
    
    autosave: function() {
        this._throttleSave = _.throttle(this.save, 1000);
        this._debounceSave = _.debounce(this.save, 5000);
    },
    
    save: function() {
        var data = this.serialize();
        $.post(window.location.href, data);
    },
    
    serialize: function() {
        var self = this;
        var data = {
            "slides": [],
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        };
        
        $(".slide-editor").each(function() {
            var text = self.slideText(this);
            var html = self.slideHtml(this);
            data["slides"].push([text, html]);
        });
        
        data["slides"] = JSON.stringify(data["slides"]);
        
        return data;
    }
    
};

$(document).ready(function() {
    
    console.log(["Slides", $('.slide-editor')]);
    $('.slide-editor').each(function() {
        console.log(["Init slide editor", this]);
        new DC.PresentationEditor({
            '$el': $(this)
        });
    });

});