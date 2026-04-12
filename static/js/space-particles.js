/* space-particles.js — animated star field */
(function () {
    "use strict";

    function init() {
        const canvas = document.createElement("canvas");
        canvas.id = "space-canvas";
        Object.assign(canvas.style, {
            position: "fixed", inset: "0", width: "100%", height: "100%",
            zIndex: "0", pointerEvents: "none"
        });
        document.body.prepend(canvas);

        const ctx = canvas.getContext("2d");
        let W, H, stars = [], nebula = [];

        function resize() {
            W = canvas.width  = window.innerWidth;
            H = canvas.height = window.innerHeight;
        }

        function rand(min, max) { return Math.random() * (max - min) + min; }

        function createStars() {
            stars = [];
            const count = Math.floor((W * H) / 4000);
            for (let i = 0; i < count; i++) {
                stars.push({
                    x: rand(0, W), y: rand(0, H),
                    r: rand(0.2, 1.8),
                    alpha: rand(0.2, 1),
                    speed: rand(0.0002, 0.001),
                    twinkle: rand(0, Math.PI * 2),
                    color: Math.random() > 0.85
                        ? `hsl(${rand(220,280)},80%,80%)`
                        : "#ffffff"
                });
            }
            // Shooting stars
            nebula = [];
            for (let i = 0; i < 3; i++) {
                nebula.push({
                    x: rand(0, W), y: rand(0, H * 0.5),
                    vx: rand(1.5, 4), vy: rand(0.5, 1.5),
                    len: rand(80, 180), alpha: 0,
                    delay: rand(0, 8000), active: false, timer: 0
                });
            }
        }

        let last = 0;
        function draw(ts) {
            const dt = ts - last; last = ts;
            ctx.clearRect(0, 0, W, H);

            // Stars
            for (const s of stars) {
                s.twinkle += s.speed * dt;
                const a = s.alpha * (0.6 + 0.4 * Math.sin(s.twinkle));
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = s.color;
                ctx.globalAlpha = a;
                ctx.fill();
            }

            // Shooting stars
            for (const n of nebula) {
                n.timer += dt;
                if (!n.active && n.timer > n.delay) {
                    n.active = true;
                    n.x = rand(0, W * 0.7);
                    n.y = rand(0, H * 0.4);
                    n.alpha = 0;
                }
                if (n.active) {
                    n.alpha = Math.min(n.alpha + 0.04, 0.9);
                    n.x += n.vx;
                    n.y += n.vy;
                    const grad = ctx.createLinearGradient(n.x, n.y, n.x - n.len, n.y - n.len * 0.4);
                    grad.addColorStop(0, `rgba(167,139,250,${n.alpha})`);
                    grad.addColorStop(1, "rgba(167,139,250,0)");
                    ctx.beginPath();
                    ctx.moveTo(n.x, n.y);
                    ctx.lineTo(n.x - n.len, n.y - n.len * 0.4);
                    ctx.strokeStyle = grad;
                    ctx.lineWidth = 1.5;
                    ctx.globalAlpha = 1;
                    ctx.stroke();
                    if (n.x > W + 50 || n.y > H + 50) {
                        n.active = false;
                        n.timer = 0;
                        n.delay = rand(3000, 10000);
                    }
                }
            }

            ctx.globalAlpha = 1;
            requestAnimationFrame(draw);
        }

        window.addEventListener("resize", () => { resize(); createStars(); });
        resize();
        createStars();
        requestAnimationFrame(draw);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
