// sponsor modal code
$(document).ready(function () {
    $('div#article_body img').parent('p').css({'text-align': 'center'});
    $('div#article_body table').addClass('table table-bordered');
    $('div#article_body thead').addClass('thead-light');
    let progressBar = new ProgressIndicator({color: '#1e90ff'});

    $('input.total_fee').change(() => {
        $('span.fee_number').text($('input.total_fee').val() / 100);
    });

    const username_validate = () => {
        const el = $('input.sponsor-username');
        let submit_el = $('button.sponsor-submit');
        el.on('change', (event) => {
            let value_length = event.delegateTarget.value.length;
            if (value_length >= 20) {
                el.addClass('breath-input');
                let username_tips = layer.tips('昵称请小于20字', el, {
                    time: 4000,
                    area: ['auto', 'auto'],
                    tips: [1, 'indianred'],
                    tipsMore: true
                });
                submit_el.attr('disabled', '');
            } else {
                el.removeClass('breath-input');
                submit_validate();
            }
        })
    };

    const message_validate = () => {
        const el = $('input.sponsor-message');
        let submit_el = $('button.sponsor-submit');
        el.on('change', (event) => {
            let value_length = event.delegateTarget.value.length;
            if (value_length >= 70) {
                el.addClass('breath-input');
                let username_tips = layer.tips('留言请小于70字', el, {
                    time: 4000,
                    area: ['auto', 'auto'],
                    tips: [1, 'indianred'],
                    tipsMore: true
                });
                submit_el.attr('disabled', '');
            } else {
                el.removeClass('breath-input');
                submit_validate();
            }
        })
    };

    const submit_validate = () => {
        const message_length = $('input.sponsor-message').val().length;
        const username_length = $('input.sponsor-username').val().length;
        let submit_el = $('button.sponsor-submit');
        if (message_length < 70 && username_length < 20) {
            submit_el.removeAttr('disabled');
        }
    };

    const init = () => {
        username_validate();
        message_validate();
    };

    init();
});

const load_sponsor_list = () => {
    let el = $('div#part-sponsor-list');
    let tbody = $('tbody#sponsors-tbody');
    const url = "/extends/sponsor-list";
    $.get(url, (res) => {
        el.remove();
        res.sponsors.forEach((item) => {
            tbody.append(
                '<tr>' +
                '<th scope="row">' + item.username + '</th>' +
                '<td>' + '<span style="font-weight: bold; color: #FF6767;">' + item.total_fee + '</span>' + '</td>' +
                '<td style="max-width: 200px;">' + item.message + '</td>' +
                '<td class="text-muted">' + item.created + '</td>' +
                '</tr>'
            )
        });
        tbody.append(
            '<tr>' +
            '<td colspan="4">' + '... <a href="/extends/sponsor-list" target="_blank">完整赞赏者名册</a>' + '</td>' +
            '</tr>'
        )
    })
};

const random_amount = () => {
    let fee = (Math.floor(Math.random() * 50) * 100);
    fee = fee < 100 ? 100 : fee;
    $('span.fee_number').text(fee / 100);
    $('input.total_fee').val(fee);
};

const close_modal = () => {
    $('div#zanshang_modal').modal('hide');
};