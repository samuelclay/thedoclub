window.DC = {};

DC.PresentationEditor = Backbone.View.extend({
    
    el: 'body',
    
    events: {
        "click input[name=submit]": "submitPresentation",
        "keyup input": "save"
    },
    
    slides: [],
    
    initialize: function() {
        this.renderPreviews();
    },
    
    renderPreviews: function() {
        var self = this;
        
        this.slides = $('.slide-editor').map(function() {
            var slide = new DC.PresentationSlideEditor({
                el: this
            });
            slide.renderPreview({skip_save: true});

            return slide;
        });
    },
    
    save: function(callback) {
        var data = this.serialize();
        $.post(window.location.href, data, _.bind(function() {
            if (_.isFunction(callback)) {
                callback();
            }
        }, this));
    },
    
    serialize: function() {
        var self = this;
        var data = {
            "slides": [],
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        };
        
        data['slides'] = JSON.stringify(_.map(this.slides, function(slide) {
            var text = slide.slideText();
            var html = slide.slideHtml();
            return [text, html];
        }));
        data["title"] = $("input[name=title]").val();
        data["description"] = $("input[name=description]").val();
        
        return data;
    },
    
    submitPresentation: function() {
        var data = this.serialize();
        data['submit'] = true;
        $.post(window.location.href, data, function() {
            window.location.href = "/presentation/choose";
        });
    }
    
});

DC.PresentationSlideEditor = Backbone.View.extend({
    
    events: {
        "keyup textarea": "renderPreview"
    },
    
    initialize: function() {
        this.text = this.slideText();
        
        this.autosave();
    },
    
    slideText: function() {
        return this.$("textarea").val();
    },
    
    slideHtml: function() {
        var text = this.slideText();
        return marked.parse(text);
    },
    
    autosave: function() {
        this._throttleSave = _.throttle(this.save, 1000);
        this._debounceSave = _.debounce(this.save, 5000);
    },
    
    renderPreview: function(options) {
        options = options || {};
        var slideHtml = this.slideHtml();
        this.$(".slide-preview").html(slideHtml);
        
        if (!options.skip_save) {
            this._throttleSave();
            this._debounceSave();
            this.$(".saved").removeClass('active');
        }
    },
    
    save: function() {
        var onPageText = this.slideText();
        
        if (onPageText != this.text) {
            this.text = onPageText;
            DC.editor.save(_.bind(function() {
                this.flashSaveMessage();
            }, this));
        }
    },
    
    flashSaveMessage: function() {
        this.$(".saved").addClass('active');
    }
    
});

$(document).ready(function() {
    DC.editor = new DC.PresentationEditor({});
});