"use strict";
/* ═══════════════════════════════════════════════════════════
   RETAIL AI — Space Particles + HUD Effects
   ═══════════════════════════════════════════════════════════ */
(function () {

    function init() {
        /* ── Canvas ── */
        const canvas = document.createElement("canvas");
        canvas.id = "space-canvas";
        Object.assign(canvas.style, {
            position: "fixed", top: "0", left: "0",
            width: "100%", height: "100%",
            zIndex: "0", pointerEvents: "none"
        });
        document.body.prepend(canvas);
        const ctx = canvas.getContext("2d");

        let W, H, stars = [], shooters = [], particles = [];
        let scanY = 0;

        /* ── Resize ── */
        function resize() {
            W = canvas.width  = window.innerWidth;
            H = canvas.height = window.innerHeight;
            buildStars();
        }

        function rand(a, b) { return Math.random() * (b - a) + a; }
        function randInt(a, b) { return Math.floor(rand(a, b)); }

        /* ── Stars ── */
        function buildStars() {
            stars = [];
            const n = Math.floor(W * H / 3500);
            for (let i = 0; i < n; i++) {
                const hue = Math.random() > 0.8 ? randInt(220, 280) : 0;
                stars.push({
                    x: rand(0, W), y: rand(0, H),
                    r: rand(0.15, 1.6),
                    base: rand(0.15, 0.9),
                    phase: rand(0, Math.PI * 2),
                    speed: rand(0.0003, 0.0012),
                    color: hue ? `hsl(${hue},70%,80%)` : "#fff"
                });
            }
            /* Shooting stars */
            shooters = [];
            for (let i = 0; i < 4; i++) {
                shooters.push(makeShooter(rand(2000, 10000)));
            }
            /* Floating particles */
            particles = [];
            for (let i = 0; i < 25; i++) {
                particles.push(makeParticle());
            }
        }

        function makeShooter(delay) {
            return {
                x: rand(0, W * 0.8), y: rand(0, H * 0.45),
                vx: rand(3, 7), vy: rand(0.8, 2.5),
                len: rand(100, 220),
                alpha: 0, alive: false,
                delay, timer: 0
            };
        }

        function makeParticle() {
            return {
                x: rand(0, W), y: rand(0, H),
                vx: rand(-0.15, 0.15), vy: rand(-0.08, -0.25),
                r: rand(1, 3),
                alpha: rand(0.1, 0.5),
                hue: randInt(220, 290)
            };
        }

        /* ── Draw loop ── */
        let last = 0;
        function draw(ts) {
            const dt = Math.min(ts - last, 50); last = ts;
            ctx.clearRect(0, 0, W, H);

            /* Stars */
            for (const s of stars) {
                s.phase += s.speed * dt;
                const a = s.base * (0.55 + 0.45 * Math.sin(s.phase));
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fillStyle = s.color;
                ctx.globalAlpha = a;
                ctx.fill();
            }

            /* Floating particles */
            for (const p of particles) {
                p.x += p.vx; p.y += p.vy;
                if (p.y < -10) { p.y = H + 10; p.x = rand(0, W); }
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = `hsl(${p.hue},80%,70%)`;
                ctx.globalAlpha = p.alpha;
                ctx.fill();
            }

            /* Shooting stars */
            for (let i = 0; i < shooters.length; i++) {
                const s = shooters[i];
                s.timer += dt;
                if (!s.alive && s.timer > s.delay) {
                    s.alive = true; s.alpha = 0;
                }
                if (s.alive) {
                    s.alpha = Math.min(s.alpha + 0.06, 0.95);
                    s.x += s.vx; s.y += s.vy;
                    const g = ctx.createLinearGradient(s.x, s.y, s.x - s.len, s.y - s.len * 0.35);
                    g.addColorStop(0, `rgba(167,139,250,${s.alpha})`);
                    g.addColorStop(0.4, `rgba(99,102,241,${s.alpha * 0.5})`);
                    g.addColorStop(1, "rgba(99,102,241,0)");
                    ctx.beginPath();
                    ctx.moveTo(s.x, s.y);
                    ctx.lineTo(s.x - s.len, s.y - s.len * 0.35);
                    ctx.strokeStyle = g;
                    ctx.lineWidth = 1.8;
                    ctx.globalAlpha = 1;
                    ctx.stroke();
                    if (s.x > W + 100 || s.y > H + 100) {
                        shooters[i] = makeShooter(rand(4000, 12000));
                    }
                }
            }

            /* HUD scan line */
            scanY = (scanY + 0.4) % H;
            const scanGrad = ctx.createLinearGradient(0, scanY - 60, 0, scanY + 60);
            scanGrad.addColorStop(0,   "rgba(99,102,241,0)");
            scanGrad.addColorStop(0.5, "rgba(99,102,241,0.04)");
            scanGrad.addColorStop(1,   "rgba(99,102,241,0)");
            ctx.fillStyle = scanGrad;
            ctx.globalAlpha = 1;
            ctx.fillRect(0, scanY - 60, W, 120);

            /* Subtle grid */
            ctx.globalAlpha = 0.025;
            ctx.strokeStyle = "#6366f1";
            ctx.lineWidth = 0.5;
            const gs = 80;
            for (let x = 0; x < W; x += gs) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
            }
            for (let y = 0; y < H; y += gs) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
            }

            ctx.globalAlpha = 1;
            requestAnimationFrame(draw);
        }

        window.addEventListener("resize", resize);
        resize();
        requestAnimationFrame(draw);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
