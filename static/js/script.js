const btnGenerate = document.querySelector("#generate-pdf");
btnGenerate.addEventListener("click",()=>{

    // Conteúdo do PDF
    const content = document.querySelector("#content-report");
    const nome = document.querySelector("#nome").textContent;
    
    // Configuração do arquivo final de PDF
    const options = {
        margin:[0, 10, 1, 10],
        filename:'apporion_${nome}_report.pdf',
        html2canvas: {scale: 2},
        jsPDF:{unit: "mm", format: "a4", orientation:"l"},
    };

    // Gerar e baixar o PDF
    html2pdf().set(options).from(content).toPdf().get("pdf").then(function (pdf){
        const pageSize = pdf.internal.pageSize;
        const contentWidth = content.offsetWidth;
        const contentHeight = content.offsetHeight;
        const scaleX = pageSize.width / contentWidth;
        const scaleY = pageSize.height / contentHeight;
        const scale = Math.min(scaleX, scaleY);

        pdf.internal.scaleFactor = scale;
        pdf.internal.scaleFactor2 = scale;
        pdf.internal.pageSize={
            width: contentWidth * scale,
            height: contentHeight * scale,
        };

        pdf.save();
    });
});