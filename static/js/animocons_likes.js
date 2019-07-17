function moving_letters(self, node_id) {
    // by @tobiasahlin

    let el = $(self).prev('.ml13');

    el.removeAttr('style');

    el.each(function () {
        $(this).html($(this).text().replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>"));
    });


    let timeline = anime.timeline({loop: false});
    timeline.add({
        targets: '.ml13_' + node_id + ' .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: function (el, i) {
            return 300 + 30 * i;
        }
    }).add({
        targets: '.ml13_' + node_id + ' .letter',
        translateY: [0, -100],
        opacity: [1, 0],
        easing: "easeInExpo",
        duration: 1200,
        delay: function (el, i) {
            return 100 + 30 * i;
        },
    });
}


// https://github.com/codrops/Animocons
const is_node_liked = (storage_json_data, node_id, node_type) => {
    const obj_type_enum = {
        ARTICLE: 'article',
        COMMENT: 'comment',
        ALBUM: 'album',
        VLOG: 'vlog'
    };
    try {
        if (node_type === obj_type_enum.COMMENT) {
            if (node_id in storage_json_data.comments && storage_json_data.comments[node_id].is_like) {
                return true
            }
        } else if (node_type === obj_type_enum.ARTICLE) {
            if (node_id in storage_json_data.articles && storage_json_data.articles[node_id].is_like) {
                return true
            }
        } else if (node_type === obj_type_enum.ALBUM) {
            if (node_id in storage_json_data.album && storage_json_data.album[node_id].is_like) {
                return true
            }
        } else if (node_type === obj_type_enum.VLOG) {
            if (node_id in storage_json_data.vlog && storage_json_data.vlog[node_id].is_like) {
                return true
            }
        } else {
            return false
        }
    } catch (e) {
        localStorage.clear();
        return false
    }

};

// validate and record likes
const increase_likes = (self, url, node_id, node_likes, node_type) => {
    let storage = window.localStorage;
    const storage_str_data = storage.getItem("dusaiphoto_data");
    let storage_json_data = JSON.parse(storage_str_data);

    // 是否存在localStorage.dusaiphoto_data
    if (!storage_json_data) {
        storage_json_data = {
            comments: {},
            articles: {},
            album: {},
            vlog: {}
        }
    }

    const node_liked_status = is_node_liked(storage_json_data, node_id, node_type);

    if (node_liked_status) {
        if (node_type === 'comment') {
            moving_letters(self, node_id);
        } else {
            layer.msg('已经点过赞了哟');
        }
        return true;
    }

    $(self).find('span.icobutton--heart').text(node_likes + 1).css('color', '#FF6767');

    $.get(url, function (result) {
        // 后台返回 success/fail
        if (result.state === 200) {

            try {
                if (result.node_type === 'comment') {
                    storage_json_data.comments[node_id] = {};
                    storage_json_data.comments[node_id]["is_like"] = true;
                } else if (result.node_type === 'article') {
                    storage_json_data.articles[node_id] = {};
                    storage_json_data.articles[node_id]["is_like"] = true;
                } else if (result.node_type === 'album') {
                    storage_json_data.album[node_id] = {};
                    storage_json_data.album[node_id]["is_like"] = true;
                } else if (result.node_type === 'vlog') {
                    storage_json_data.vlog[node_id] = {};
                    storage_json_data.vlog[node_id]["is_like"] = true;
                }
            } catch (e) {
                localStorage.clear();
            }


            const d = JSON.stringify(storage_json_data);
            try {
                storage.setItem("dusaiphoto_data", d);
            } catch (e) {
                // QUOTA_EXCEEDED_ERR_CODE = 22
                if (e.code === 22) {
                    localStorage.clear();
                    storage.setItem("dusaiphoto_data", d);
                }
            }
        } else {
            layer.msg('与服务器通信失败..过一会儿再试试吧~');
        }
    });
};

// run animation
const animocons = (self) => {
    var el = $(self), elspan = el.find('i');
    var opacityCurve16 = mojs.easing.path('M0,0 L25.333,0 L75.333,100 L100,0');
    var translationCurve16 = mojs.easing.path('M0,100h25.3c0,0,6.5-37.3,15-56c12.3-27,35-44,35-44v150c0,0-1.1-12.2,9.7-33.3c9.7-19,15-22.9,15-22.9');
    var squashCurve16 = mojs.easing.path('M0,100.004963 C0,100.004963 25,147.596355 25,100.004961 C25,70.7741867 32.2461944,85.3230873 58.484375,94.8579105 C68.9280825,98.6531013 83.2611815,99.9999999 100,100');

    let timeline = new mojs.Timeline();

    let tweens1 = new mojs.Burst({
        parent: el,
        count: 6,
        radius: {0: 150},
        degree: 50,
        angle: -25,
        opacity: 0.3,
        children: {
            fill: '#FF6767',
            scale: 1,
            radius: {'rand(5,15)': 0},
            duration: 1700,
            delay: 350,
            easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
        },

    });
    let tweens2 = new mojs.Burst({
        parent: el,
        count: 3,
        degree: 0,
        radius: {80: 250},
        angle: 180,
        children: {
            top: [45, 0, 45],
            left: [-15, 0, 15],
            shape: 'line',
            radius: {60: 0},
            scale: 1,
            stroke: '#FF6767',
            opacity: 0.4,
            duration: 650,
            delay: 200,
            easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
        },

    });
    // icon scale animation
    let tweens3 = new mojs.Tween({
        duration: 500,
        onUpdate: function (progress) {
            let translateProgress = translationCurve16(progress),
                squashProgress = squashCurve16(progress),
                scaleX = 1 - 2 * squashProgress,
                scaleY = 1 + 2 * squashProgress;

            elspan.css('transform', 'translate3d(0,' + -180 * translateProgress + 'px,0) scale3d(' + scaleX + ',' + scaleY + ',1)');

            let opacityProgress = opacityCurve16(progress);
            elspan.css('opacity', opacityProgress);

            el.css('color', progress >= 0.75 ? '#FF6767' : '#C0C1C3');
        },

    });

    timeline.add(tweens1, tweens2, tweens3);
    timeline.replay();

    window.setTimeout(clear_element.bind(null, el), 1500)
};

// 清除shape元素
const clear_element = (el) => {
    const animation_el = $(el).find('[data-name=mojs-shape]');
    animation_el.remove();
};

// increase likes handler
const animocons_handler = (self, url, node_id, node_likes, node_type) => {
    const is_liked = increase_likes(self, url, node_id, node_likes, node_type);
    if (!is_liked) {
        animocons($(self).find('.icobutton'));
    }
};

// 点赞初始渲染
$(() => {
    const item_get_color = (el) => {
        el.css('color', '#FF6767');
        el.prev('.icobutton').css('color', '#FF6767');
    };

    let storage = window.localStorage;
    const storage_str_data = storage.getItem("dusaiphoto_data");
    let storage_json_data = JSON.parse(storage_str_data);
    if (storage_json_data) {
        $('span.icobutton--heart').each(function (index, element) {
            let item = $(element);
            let node_id = item.attr('data-id');
            let node_type = item.attr('data-type');

            const node_liked_status = is_node_liked(storage_json_data, node_id, node_type);
            if (node_liked_status) {
                item_get_color(item)
            }
        });
    }
});
