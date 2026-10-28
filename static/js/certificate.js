/**
 * Surakshaa Saathi — Automatic High-Resolution Certificate Generator
 * Awards Certificate of Appreciation (S >= T - 2) or Participation (Otherwise).
 * Exports to High-Resolution PDF (via jsPDF) and PNG (via HTML5 Canvas).
 */

class CertificateManager {
  constructor() {
    this.currentCert = null;
  }

  generateCertificateData(participantName, score, totalMarks, quizDate, certNumber) {
    const isAppreciation = score >= (totalMarks - 2);
    const title = isAppreciation ? "Certificate of Appreciation" : "Certificate of Participation";
    const titleHindi = isAppreciation ? "प्रशंसा प्रमाणपत्र" : "सहभागिता प्रमाणपत्र";

    const appreciationMsg = "In recognition of outstanding dedication and exceptional mastery in digital safety, scam defense, and cyber fraud prevention demonstrated during the National Cyber Awareness Examination.";
    const participationMsg = "In recognition of proactive participation and commendable commitment to personal and community digital defense during the National Cyber Awareness Examination.";

    return {
      participantName: participantName || "Dedicated Citizen",
      title: title,
      titleHindi: titleHindi,
      score: score,
      totalMarks: totalMarks,
      percentage: Math.round((score / totalMarks) * 100),
      quizDate: quizDate || new Date().toISOString().split("T")[0],
      issueDate: quizDate || new Date().toISOString().split("T")[0],
      certificateNumber: certNumber || ("SS-2026-" + Math.random().toString(16).substring(2, 10).toUpperCase()),
      message: isAppreciation ? appreciationMsg : participationMsg,
      isAppreciation: isAppreciation
    };
  }

  renderToCanvas(certData, canvasElement) {
    this.currentCert = certData;
    const canvas = canvasElement || document.getElementById("cert-preview-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const width = 1600;
    const height = 1130;
    canvas.width = width;
    canvas.height = height;

    // Background: Cream / Pearl white parchment texture with gentle gradient
    const bgGrad = ctx.createLinearGradient(0, 0, width, height);
    bgGrad.addColorStop(0, "#FBFBFE");
    bgGrad.addColorStop(0.5, "#F7F8FC");
    bgGrad.addColorStop(1, "#EFF1F9");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, width, height);

    // Subtle guilloche security watermark pattern in background
    ctx.save();
    ctx.strokeStyle = "rgba(10, 14, 39, 0.025)";
    ctx.lineWidth = 1;
    for (let r = 80; r < 550; r += 28) {
      ctx.beginPath();
      ctx.arc(width / 2, height / 2 + 30, r, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.restore();

    // Outer Decorative Border: Deep Indigo & Gold Accents
    ctx.strokeStyle = "#0A0E27";
    ctx.lineWidth = 16;
    ctx.strokeRect(30, 30, width - 60, height - 60);

    ctx.strokeStyle = certData.isAppreciation ? "#F59E0B" : "#06B6D4"; // Gold or Teal
    ctx.lineWidth = 4;
    ctx.strokeRect(48, 48, width - 96, height - 96);

    ctx.strokeStyle = "rgba(10, 14, 39, 0.2)";
    ctx.lineWidth = 1.5;
    ctx.strokeRect(58, 58, width - 116, height - 116);

    // Ornate Corner Brackets
    const drawCorner = (x, y, flipX, flipY) => {
      ctx.save();
      ctx.translate(x, y);
      ctx.scale(flipX ? -1 : 1, flipY ? -1 : 1);
      ctx.fillStyle = certData.isAppreciation ? "#F59E0B" : "#06B6D4";
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(45, 0);
      ctx.lineTo(45, 12);
      ctx.lineTo(12, 12);
      ctx.lineTo(12, 45);
      ctx.lineTo(0, 45);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    };
    drawCorner(68, 68, false, false);
    drawCorner(width - 68, 68, true, false);
    drawCorner(68, height - 68, false, true);
    drawCorner(width - 68, height - 68, true, true);

    // Header Emblem & Brand
    ctx.textAlign = "center";
    ctx.fillStyle = "#0A0E27";
    ctx.font = "bold 32px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("SURAKSHAA SAATHI", width / 2, 140);

    ctx.fillStyle = certData.isAppreciation ? "#B45309" : "#0891B2";
    ctx.font = "600 18px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("NATIONAL CYBER AWARENESS & PUBLIC SAFETY INITIATIVE", width / 2, 175);

    ctx.strokeStyle = "#D1D5DB";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(width / 2 - 280, 195);
    ctx.lineTo(width / 2 + 280, 195);
    ctx.stroke();

    // Certificate Title
    ctx.fillStyle = "#0A0E27";
    ctx.font = "bold 52px 'Times New Roman', serif";
    ctx.fillText(certData.title.toUpperCase(), width / 2, 275);

    ctx.fillStyle = "#4B5563";
    ctx.font = "italic 22px 'Segoe UI', Arial, sans-serif";
    ctx.fillText(certData.titleHindi, width / 2, 315);

    ctx.fillStyle = "#374151";
    ctx.font = "20px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("THIS OFFICIAL CERTIFICATE IS PROUDLY PRESENTED TO", width / 2, 390);

    // Participant Full Name
    ctx.fillStyle = "#0A0E27";
    ctx.font = "bold 56px 'Times New Roman', Georgia, serif";
    ctx.fillText(certData.participantName, width / 2, 480);

    // Name Underline with Center Star
    ctx.strokeStyle = certData.isAppreciation ? "#F59E0B" : "#06B6D4";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(width / 2 - 320, 510);
    ctx.lineTo(width / 2 - 20, 510);
    ctx.moveTo(width / 2 + 20, 510);
    ctx.lineTo(width / 2 + 320, 510);
    ctx.stroke();

    // Message Body
    ctx.fillStyle = "#4B5563";
    ctx.font = "21px 'Segoe UI', Arial, sans-serif";
    const words = certData.message.split(" ");
    let line = "";
    let yPos = 565;
    for (let w of words) {
      if ((line + w).length > 82) {
        ctx.fillText(line, width / 2, yPos);
        line = w + " ";
        yPos += 34;
      } else {
        line += w + " ";
      }
    }
    if (line) ctx.fillText(line, width / 2, yPos);

    // Score & Marks Box
    const boxY = 660;
    ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
    ctx.strokeStyle = "#E5E7EB";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(width / 2 - 260, boxY, 520, 75, 12);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#0A0E27";
    ctx.font = "bold 22px 'Segoe UI', Arial, sans-serif";
    ctx.fillText(`Examination Score: ${certData.score} / ${certData.totalMarks} Marks (${certData.percentage}%)`, width / 2, boxY + 38);

    ctx.fillStyle = certData.isAppreciation ? "#16A34A" : "#0284C7";
    ctx.font = "600 16px 'Segoe UI', Arial, sans-serif";
    ctx.fillText(`Evaluation Standard: ${certData.isAppreciation ? "Honors Tier (Top Performance)" : "Certified Participation Standard"}`, width / 2, boxY + 62);

    // Decorative Gold / Teal Seal
    const sealX = 250;
    const sealY = 880;
    ctx.save();
    ctx.translate(sealX, sealY);
    ctx.beginPath();
    ctx.arc(0, 0, 70, 0, Math.PI * 2);
    ctx.fillStyle = certData.isAppreciation ? "#F59E0B" : "#06B6D4";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(0, 0, 60, 0, Math.PI * 2);
    ctx.strokeStyle = "#FFFFFF";
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 13px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("NATIONAL", 0, -25);
    ctx.font = "bold 16px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("VERIFIED", 0, -2);
    ctx.font = "bold 12px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("CYBER DEFENSE", 0, 22);
    ctx.restore();

    // Signatures & Metadata Footer
    ctx.textAlign = "center";
    // Left: Verification & Date
    ctx.fillStyle = "#111827";
    ctx.font = "bold 18px 'Segoe UI', Arial, sans-serif";
    ctx.fillText(certData.issueDate, 550, 895);
    ctx.strokeStyle = "#9CA3AF";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(430, 910);
    ctx.lineTo(670, 910);
    ctx.stroke();
    ctx.fillStyle = "#6B7280";
    ctx.font = "16px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("Date of Issue & IST Record", 550, 935);

    // Right: Authorized Signatory
    ctx.fillStyle = "#111827";
    ctx.font = "italic bold 22px 'Times New Roman', serif";
    ctx.fillText("Dr. K. S. Verma, Ph.D.", 1080, 895);
    ctx.strokeStyle = "#9CA3AF";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(960, 910);
    ctx.lineTo(1200, 910);
    ctx.stroke();
    ctx.fillStyle = "#6B7280";
    ctx.font = "16px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("Director of Public Cyber Safety Education", 1080, 935);

    // Unique Certificate Reference
    ctx.textAlign = "center";
    ctx.fillStyle = "#374151";
    ctx.font = "600 17px monospace";
    ctx.fillText(`Certificate ID: ${certData.certificateNumber}  •  Verify at: https://cybercrime.gov.in`, width / 2, 1025);

    ctx.fillStyle = "#9CA3AF";
    ctx.font = "14px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("Stay Aware. Stay Secure. Stay Ahead. — Surakshaa Saathi Digital Shield", width / 2, 1055);
  }

  downloadPNG(certData) {
    const canvas = document.getElementById("cert-preview-canvas");
    if (!canvas) return;
    const link = document.createElement("a");
    link.download = `Surakshaa_Saathi_Certificate_${certData.certificateNumber}.png`;
    link.href = canvas.toDataURL("image/png", 1.0);
    link.click();
  }

  downloadPDF(certData) {
    const canvas = document.getElementById("cert-preview-canvas");
    if (!canvas) return;

    // Use window.jspdf if loaded, or fallback to direct canvas PNG export
    if (window.jspdf && window.jspdf.jsPDF) {
      const { jsPDF } = window.jspdf;
      // Landscape A4 orientation
      const pdf = new jsPDF({
        orientation: "landscape",
        unit: "mm",
        format: "a4"
      });
      const imgData = canvas.toDataURL("image/png", 0.95);
      pdf.addImage(imgData, "PNG", 0, 0, 297, 210);
      pdf.save(`Surakshaa_Saathi_${certData.certificateNumber}.pdf`);
    } else {
      // Direct PNG fallback
      this.downloadPNG(certData);
    }
  }

  async sendEmail(certNumber) {
    try {
      const resp = await fetch(`/api/certificates/${certNumber}/send-email`, {
        method: "POST"
      });
      const data = await resp.json();
      return data;
    } catch (e) {
      return { status: "error", message: e.message };
    }
  }
}

window.certificateManager = new CertificateManager();

