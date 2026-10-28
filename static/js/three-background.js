/**
 * Surakshaa Saathi — Signature 3D Moving Background & Interactive Particle Ribbon
 * Multilayered Aurora Gradients, 3D Curved Energy Ribbon, Floating Geometric Shield,
 * Interconnected Digital Nodes & Parallax Depth.
 */

class Surakshaa3DBackground {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");

    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.dpr = Math.min(window.devicePixelRatio || 1, 2);

    this.reducedMotion = localStorage.getItem("surakshaa_reduced_motion") === "true";
    this.mouseX = this.width / 2;
    this.mouseY = this.height / 2;
    this.targetMouseX = this.mouseX;
    this.targetMouseY = this.mouseY;

    this.time = 0;
    this.particles = [];
    this.shieldVertices = [];
    this.shieldRotation = 0;
    this.shieldOpacity = 0.4;
    this.shieldPulse = 0;

    this.initCanvas();
    this.initParticles();
    this.initShield();
    this.bindEvents();
    this.animate();
  }

  initCanvas() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.canvas.width = this.width * this.dpr;
    this.canvas.height = this.height * this.dpr;
    this.ctx.scale(this.dpr, this.dpr);
  }

  initParticles() {
    this.particles = [];
    const count = window.innerWidth < 768 ? 45 : 85;
    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        z: Math.random() * 2 + 0.5, // Depth factor
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 2 + 1,
        color: i % 4 === 0 ? "rgba(6, 182, 212, " : // Teal
               i % 4 === 1 ? "rgba(124, 58, 237, " : // Violet
               i % 4 === 2 ? "rgba(16, 185, 129, " : // Emerald
                             "rgba(245, 158, 11, ",   // Amber
        alpha: Math.random() * 0.5 + 0.2
      });
    }
  }

  initShield() {
    // 3D Wireframe Hexagonal / Shield Geometry Vertices
    // [x, y, z] coordinates centered around origin
    this.shieldVertices = [
      [0, -140, 0],       // Top apex
      [85, -80, 20],      // Upper right
      [105, 30, -10],     // Mid right
      [0, 150, 40],       // Bottom point
      [-105, 30, -10],    // Mid left
      [-85, -80, 20],     // Upper left
      // Inner core emblem
      [0, -70, 30],
      [45, -30, 40],
      [0, 80, 50],
      [-45, -30, 40]
    ];
  }

  bindEvents() {
    window.addEventListener("resize", () => {
      this.initCanvas();
      this.initParticles();
    });

    window.addEventListener("mousemove", (e) => {
      this.targetMouseX = e.clientX;
      this.targetMouseY = e.clientY;
    });

    window.addEventListener("touchmove", (e) => {
      if (e.touches && e.touches[0]) {
        this.targetMouseX = e.touches[0].clientX;
        this.targetMouseY = e.touches[0].clientY;
      }
    }, { passive: true });
  }

  setReducedMotion(enabled) {
    this.reducedMotion = enabled;
    localStorage.setItem("surakshaa_reduced_motion", enabled);
  }

  drawAurora() {
    // Multilayered flowing atmospheric light gradients
    const t = this.time * 0.0006;
    const g1x = this.width * 0.3 + Math.sin(t) * 180;
    const g1y = this.height * 0.3 + Math.cos(t * 0.8) * 120;
    const g2x = this.width * 0.75 + Math.cos(t * 1.2) * 160;
    const g2y = this.height * 0.65 + Math.sin(t * 0.9) * 140;

    // Gradient 1: Deep Violet / Indigo
    const grad1 = this.ctx.createRadialGradient(g1x, g1y, 30, g1x, g1y, this.width * 0.6);
    grad1.addColorStop(0, "rgba(124, 58, 237, 0.16)"); // Electric violet
    grad1.addColorStop(0.5, "rgba(10, 14, 39, 0.08)");
    grad1.addColorStop(1, "rgba(10, 14, 39, 0)");
    this.ctx.fillStyle = grad1;
    this.ctx.fillRect(0, 0, this.width, this.height);

    // Gradient 2: Luminous Teal / Emerald
    const grad2 = this.ctx.createRadialGradient(g2x, g2y, 40, g2x, g2y, this.width * 0.55);
    grad2.addColorStop(0, "rgba(6, 182, 212, 0.14)"); // Luminous teal
    grad2.addColorStop(0.4, "rgba(16, 185, 129, 0.08)"); // Emerald
    grad2.addColorStop(1, "rgba(10, 14, 39, 0)");
    this.ctx.fillStyle = grad2;
    this.ctx.fillRect(0, 0, this.width, this.height);
  }

  drawEnergyRibbon() {
    // 3D undulating energy ribbon traversing across the screen
    const ctx = this.ctx;
    const t = this.time * 0.001;
    const segments = 60;
    const step = this.width / segments;

    ctx.save();
    ctx.lineWidth = 2.5;

    // Draw primary teal ribbon
    ctx.beginPath();
    for (let i = 0; i <= segments; i++) {
      const x = i * step;
      // Layered sine harmonic waves
      const wave1 = Math.sin(x * 0.003 + t) * 85;
      const wave2 = Math.cos(x * 0.007 - t * 0.8) * 45;
      const y = (this.height * 0.55) + wave1 + wave2;

      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    const ribbonGrad = ctx.createLinearGradient(0, 0, this.width, this.height);
    ribbonGrad.addColorStop(0, "rgba(6, 182, 212, 0)");
    ribbonGrad.addColorStop(0.3, "rgba(6, 182, 212, 0.35)");
    ribbonGrad.addColorStop(0.6, "rgba(124, 58, 237, 0.35)");
    ribbonGrad.addColorStop(1, "rgba(16, 185, 129, 0)");
    ctx.strokeStyle = ribbonGrad;
    ctx.shadowColor = "rgba(6, 182, 212, 0.5)";
    ctx.shadowBlur = 12;
    ctx.stroke();

    // Secondary subtle ribbon
    ctx.beginPath();
    for (let i = 0; i <= segments; i++) {
      const x = i * step;
      const wave1 = Math.sin(x * 0.004 - t * 1.2) * 65;
      const wave2 = Math.cos(x * 0.002 + t * 0.5) * 35;
      const y = (this.height * 0.58) + wave1 + wave2;

      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = "rgba(168, 85, 247, 0.22)";
    ctx.lineWidth = 1.5;
    ctx.shadowBlur = 8;
    ctx.stroke();

    ctx.restore();
  }

  drawShield() {
    // 3D Holographic Protective Shield in Center/Hero
    const ctx = this.ctx;
    const centerX = this.width * 0.72; // Placed aesthetically behind hero visual
    const centerY = this.height * 0.42;

    this.shieldRotation += this.reducedMotion ? 0 : 0.004;
    this.shieldPulse = Math.sin(this.time * 0.0015);
    const scale = 1.0 + this.shieldPulse * 0.04;

    const rotY = this.shieldRotation;
    const rotX = Math.sin(this.time * 0.0008) * 0.2;

    // Project 3D vertices to 2D screen coordinates
    const projected = this.shieldVertices.map(v => {
      let x = v[0] * scale;
      let y = v[1] * scale;
      let z = v[2] * scale;

      // Rotate around Y axis
      const cosY = Math.cos(rotY);
      const sinY = Math.sin(rotY);
      const x1 = x * cosY - z * sinY;
      const z1 = z * cosY + x * sinY;

      // Rotate around X axis
      const cosX = Math.cos(rotX);
      const sinX = Math.sin(rotX);
      const y2 = y * cosX - z1 * sinX;
      const z2 = z1 * cosX + y * sinX;

      // Perspective projection
      const fov = 450;
      const pScale = fov / (fov + z2 + 80);
      return [centerX + x1 * pScale, centerY + y2 * pScale, pScale];
    });

    ctx.save();
    ctx.lineWidth = 1.5;

    // Outer shield contour
    ctx.beginPath();
    const outerIndices = [0, 1, 2, 3, 4, 5, 0];
    outerIndices.forEach((idx, i) => {
      const p = projected[idx];
      if (i === 0) ctx.moveTo(p[0], p[1]);
      else ctx.lineTo(p[0], p[1]);
    });
    ctx.strokeStyle = `rgba(6, 182, 212, ${0.28 + this.shieldPulse * 0.1})`;
    ctx.shadowColor = "rgba(6, 182, 212, 0.4)";
    ctx.shadowBlur = 10;
    ctx.stroke();

    // Inner core emblem contour
    ctx.beginPath();
    const innerIndices = [6, 7, 8, 9, 6];
    innerIndices.forEach((idx, i) => {
      const p = projected[idx];
      if (i === 0) ctx.moveTo(p[0], p[1]);
      else ctx.lineTo(p[0], p[1]);
    });
    ctx.strokeStyle = `rgba(16, 185, 129, ${0.35 + this.shieldPulse * 0.1})`;
    ctx.stroke();

    // Cross connecting lines
    ctx.beginPath();
    ctx.moveTo(projected[0][0], projected[0][1]);
    ctx.lineTo(projected[8][0], projected[8][1]);
    ctx.moveTo(projected[5][0], projected[5][1]);
    ctx.lineTo(projected[7][0], projected[7][1]);
    ctx.moveTo(projected[1][0], projected[1][1]);
    ctx.lineTo(projected[9][0], projected[9][1]);
    ctx.strokeStyle = "rgba(124, 58, 237, 0.18)";
    ctx.stroke();

    // Vertex glowing nodes
    projected.forEach(p => {
      ctx.beginPath();
      ctx.arc(p[0], p[1], 2.5 * p[2], 0, Math.PI * 2);
      ctx.fillStyle = "rgba(245, 158, 11, 0.85)";
      ctx.fill();
    });

    ctx.restore();
  }

  drawParticles() {
    const ctx = this.ctx;
    // Mouse Parallax offset
    this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
    this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;
    const parallaxX = (this.mouseX - this.width / 2) * 0.04;
    const parallaxY = (this.mouseY - this.height / 2) * 0.04;

    this.particles.forEach(p => {
      if (!this.reducedMotion) {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x = this.width;
        if (p.x > this.width) p.x = 0;
        if (p.y < 0) p.y = this.height;
        if (p.y > this.height) p.y = 0;
      }

      const drawX = p.x + parallaxX * p.z;
      const drawY = p.y + parallaxY * p.z;

      ctx.beginPath();
      ctx.arc(drawX, drawY, p.radius * p.z, 0, Math.PI * 2);
      ctx.fillStyle = p.color + p.alpha + ")";
      ctx.fill();
    });

    // Draw delicate network lines between close particles
    ctx.lineWidth = 0.6;
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 110) {
          const alpha = (1 - dist / 110) * 0.12;
          ctx.beginPath();
          ctx.moveTo(p1.x + parallaxX * p1.z, p1.y + parallaxY * p1.z);
          ctx.lineTo(p2.x + parallaxX * p2.z, p2.y + parallaxY * p2.z);
          ctx.strokeStyle = `rgba(6, 182, 212, ${alpha})`;
          ctx.stroke();
        }
      }
    }
  }

  animate() {
    this.time += this.reducedMotion ? 0.3 : 1.0;

    // Clear background with midnight indigo
    this.ctx.fillStyle = "#0A0E27";
    this.ctx.fillRect(0, 0, this.width, this.height);

    this.drawAurora();
    this.drawEnergyRibbon();
    if (this.width > 640) {
      this.drawShield();
    }
    this.drawParticles();

    requestAnimationFrame(() => this.animate());
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.surakshaa3D = new Surakshaa3DBackground("surakshaa-3d-canvas");
});

