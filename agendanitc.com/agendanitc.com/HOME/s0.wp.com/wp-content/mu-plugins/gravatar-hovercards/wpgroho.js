WPGroHo = jQuery.extend({
    my_hash: '',
    data: {},
    renderers: {},
    syncProfileData: function(hash, id) {
        if (!WPGroHo.data[hash]) {
            WPGroHo.data[hash] = {};
            a = jQuery('div.grofile-hash-map-' + hash + ' span').each(function() {
                WPGroHo.data[hash][this.className] = jQuery(this).text();
            });
        }
        WPGroHo.appendProfileData(WPGroHo.data[hash], hash, id);
    },
    appendProfileData: function(data, hash, id) {
        for (var key in data) {
            if (jQuery.isFunction(WPGroHo.renderers[key])) {
                return WPGroHo.renderers[key](data[key], hash, id, key);
            }
            jQuery('#' + id).find('h4').after(jQuery('<p class="grav-extra ' + key + '" />').html(data[key]));
        }
    }
}, WPGroHo);