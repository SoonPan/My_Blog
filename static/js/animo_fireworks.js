// https://github.com/codrops/Animocons
$(() => {
    var molinkEl = document.querySelector('.animo_fireworks'),
        moTimeline = new mojs.Timeline(),
        moburst1 = new mojs.Burst({
            parent: molinkEl,
            count: 6,
            left: '0%',
            top: '-50%',
            radius: {0: 60},
            children: {
                fill: ['#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE'],
                duration: 1300,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }
        }),
        moburst2 = new mojs.Burst({
            parent: molinkEl,
            left: '-100%', top: '-20%',
            count: 14,
            radius: {0: 120},
            children: {
                fill: ['#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE'],
                duration: 1600,
                delay: 100,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }
        }),
        moburst3 = new mojs.Burst({
            parent: molinkEl,
            left: '130%', top: '-70%',
            count: 8,
            radius: {0: 90},
            children: {
                fill: ['#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE'],
                duration: 1500,
                delay: 200,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }
        }),
        moburst4 = new mojs.Burst({
            parent: molinkEl,
            left: '-20%', top: '-150%',
            count: 14,
            radius: {0: 60},
            children: {
                fill: ['#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE'],
                duration: 2000,
                delay: 300,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }
        }),
        moburst5 = new mojs.Burst({
            parent: molinkEl,
            count: 12,
            left: '30%', top: '-100%',
            radius: {0: 60},
            children: {
                fill: ['#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE'],
                duration: 1400,
                delay: 400,
                easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
            }
        });

    moTimeline.add(moburst1, moburst2, moburst3, moburst4, moburst5);
    molinkEl.addEventListener('mouseenter', function () {
        moTimeline.replay();
    });
});