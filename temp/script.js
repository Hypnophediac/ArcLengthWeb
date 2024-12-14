const canvas = document.getElementById('arcCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size with proper resolution
function resizeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
}

// Call resize on load and window resize
window.addEventListener('load', resizeCanvas);
window.addEventListener('resize', resizeCanvas);

function drawBendingVisualization(outerRadius, neutralRadius, innerRadius, totalAngle, bends, startLength, endLength) {
    const canvas = document.getElementById('arcCanvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Calculate angles in radians
    const startAngle = -Math.PI/2; // -90 degrees
    const endAngle = startAngle + (totalAngle * Math.PI/180);
    
    // Calculate total dimensions including all components
    const arcWidth = 2 * outerRadius * Math.sin(totalAngle * Math.PI / 360);
    const arcHeight = outerRadius * (1 - Math.cos(totalAngle * Math.PI / 360));
    
    // Calculate total width including straight segments
    const totalWidth = arcWidth + startLength + endLength;
    const totalHeight = Math.max(arcHeight * 2, outerRadius * 2);
    
    // Calculate scale to fit both width and height with padding
    const padding = 50; // Padding from canvas edges
    const scaleX = (canvas.width - 2 * padding) / totalWidth;
    const scaleY = (canvas.height - 2 * padding) / totalHeight;
    const scale = Math.min(scaleX, scaleY);
    
    // Calculate center point to center the drawing
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    // Adjust vertical position based on the bend angle
    const verticalOffset = (arcHeight * scale) / 2;
    const adjustedCenterY = centerY + verticalOffset;
    
    // Draw coordinate system
    ctx.strokeStyle = '#ccc';
    ctx.beginPath();
    ctx.moveTo(50, adjustedCenterY);
    ctx.lineTo(canvas.width - 50, adjustedCenterY);
    ctx.moveTo(centerX, 50);
    ctx.lineTo(centerX, canvas.height - 50);
    ctx.stroke();
    
    // Increase font size for better visibility with larger scale
    ctx.font = '16px Arial';
    
    // Calculate start and end points
    const arcStartX = centerX + innerRadius * scale * Math.cos(startAngle);
    const arcStartY = adjustedCenterY + innerRadius * scale * Math.sin(startAngle);
    const arcEndX = centerX + innerRadius * scale * Math.cos(endAngle);
    const arcEndY = adjustedCenterY + innerRadius * scale * Math.sin(endAngle);
    
    // Calculate and draw start segment
    if (startLength > 0) {
        // Calculate start point by moving in the direction perpendicular to the first bend
        // Adjust the angle to create the correct central angle
        const startSegmentAngle = startAngle - Math.PI/2; // 90 degrees counter-clockwise from the start angle
        const startX = arcStartX + startLength * Math.cos(startSegmentAngle);
        const startY = arcStartY + startLength * Math.sin(startSegmentAngle);
        
        ctx.strokeStyle = '#FF9800'; // Orange for start segment
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(arcStartX, arcStartY);
        ctx.stroke();
        
        // Label start segment
        ctx.save();
        const labelX = (startX + arcStartX) / 2;
        const labelY = (startY + arcStartY) / 2;
        ctx.translate(labelX, labelY);
        ctx.rotate(startSegmentAngle);
        ctx.fillStyle = '#FF9800';
        ctx.textAlign = 'center';
        ctx.fillText(`${startLength.toFixed(1)}mm`, 0, -10);
        ctx.restore();

        // Draw the angle between start segment and first chord
        if (bends.length > 1) {
            const nextProgress = 1 / (bends.length - 1);
            const nextAngle = startAngle + (endAngle - startAngle) * nextProgress;
            
            // Draw angle arc - showing the central angle
            ctx.beginPath();
            ctx.strokeStyle = '#000';
            const angleRadius = 30;
            ctx.arc(arcStartX, arcStartY, angleRadius, startSegmentAngle, startAngle, false);
            ctx.stroke();
            
            // Calculate midpoint angle for the text
            const midAngle = (startSegmentAngle + startAngle) / 2;
            const textRadius = angleRadius + 10;
            const textX = arcStartX + textRadius * Math.cos(midAngle);
            const textY = arcStartY + textRadius * Math.sin(midAngle);
            
            // Draw angle text - show the central angle
            ctx.fillStyle = '#000';
            ctx.textAlign = 'center';
            ctx.fillText(`${bends[0].centralAngle.toFixed(1)}°`, textX, textY);
        }
    }
    
    // Draw outer arc (green)
    ctx.strokeStyle = '#4CAF50';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.arc(centerX, adjustedCenterY, outerRadius * scale, startAngle, endAngle);
    ctx.stroke();
    
    // Draw neutral arc (blue)
    ctx.strokeStyle = '#2196F3';
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.arc(centerX, adjustedCenterY, neutralRadius * scale, startAngle, endAngle);
    ctx.stroke();
    
    // Draw inner arc (red)
    ctx.strokeStyle = '#f44336';
    ctx.beginPath();
    ctx.arc(centerX, adjustedCenterY, innerRadius * scale, startAngle, endAngle);
    ctx.stroke();
    
    // Draw end segment
    if (endLength > 0) {
        // Calculate end point by extending perpendicular to the last bend
        const endSegmentAngle = endAngle + Math.PI/2; // 90 degrees clockwise from the end angle
        const endX = arcEndX + endLength * Math.cos(endSegmentAngle);
        const endY = arcEndY + endLength * Math.sin(endSegmentAngle);
        
        ctx.strokeStyle = '#9C27B0'; // Purple for end segment
        ctx.beginPath();
        ctx.moveTo(arcEndX, arcEndY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
        
        // Label end segment
        ctx.save();
        ctx.translate((arcEndX + endX) / 2, (arcEndY + endY) / 2);
        ctx.rotate(endSegmentAngle);
        ctx.fillStyle = '#9C27B0';
        ctx.fillText(`${endLength.toFixed(1)}mm`, 0, -10);
        ctx.restore();

        // Draw the angle between last chord and end segment
        if (bends.length > 1) {
            const prevProgress = (bends.length - 2) / (bends.length - 1);
            const prevAngle = startAngle + (endAngle - startAngle) * prevProgress;
            
            // Draw angle arc for the central angle
            ctx.beginPath();
            ctx.strokeStyle = '#000';
            const angleRadius = 30;
            ctx.arc(arcEndX, arcEndY, angleRadius, endAngle, endSegmentAngle, false);
            ctx.stroke();
            
            // Calculate midpoint angle for the text
            const midAngle = (endAngle + endSegmentAngle) / 2;
            const textRadius = angleRadius + 10;
            const textX = arcEndX + textRadius * Math.cos(midAngle);
            const textY = arcEndY + textRadius * Math.sin(midAngle);
            
            // Draw angle text - show the central angle
            ctx.fillStyle = '#000';
            ctx.textAlign = 'center';
            ctx.fillText(`${bends[bends.length - 1].centralAngle.toFixed(1)}°`, textX, textY);
        }
    }
    
    // Draw middle bends
    let currentAngle = 0;
    for (let i = 0; i < bends.length; i++) {
        const bend = bends[i];
        
        // Calculate the angle for this bend point
        const progress = i / (bends.length - 1);
        const bendAngleInRadians = startAngle + (endAngle - startAngle) * progress;
        
        // Calculate bend point coordinates
        const bendX = centerX + innerRadius * scale * Math.cos(bendAngleInRadians);
        const bendY = adjustedCenterY + innerRadius * scale * Math.sin(bendAngleInRadians);
        
        // Draw radius line
        ctx.beginPath();
        ctx.moveTo(
            centerX + innerRadius * scale * Math.cos(bendAngleInRadians),
            adjustedCenterY + innerRadius * scale * Math.sin(bendAngleInRadians)
        );
        ctx.lineTo(
            centerX + outerRadius * scale * Math.cos(bendAngleInRadians),
            adjustedCenterY + outerRadius * scale * Math.sin(bendAngleInRadians)
        );
        ctx.stroke();

        // Draw bending point marker (circle)
        ctx.beginPath();
        ctx.fillStyle = '#FF0000';  // Red color for bending points
        ctx.arc(
            centerX + innerRadius * scale * Math.cos(bendAngleInRadians),
            adjustedCenterY + innerRadius * scale * Math.sin(bendAngleInRadians),
            5,  // Radius of the marker circle
            0,
            2 * Math.PI
        );
        ctx.fill();
        ctx.strokeStyle = '#000';  // Black border
        ctx.stroke();
        
        // Draw chord to next bend point if not the last point
        if (i < bends.length - 1) {
            const nextProgress = (i + 1) / (bends.length - 1);
            const nextAngle = startAngle + (endAngle - startAngle) * nextProgress;
            const nextX = centerX + innerRadius * scale * Math.cos(nextAngle);
            const nextY = adjustedCenterY + innerRadius * scale * Math.sin(nextAngle);
            
            // Draw chord line
            ctx.beginPath();
            ctx.strokeStyle = '#FFA000'; // Orange color for chords
            ctx.setLineDash([2, 2]); // Dashed line for chords
            ctx.moveTo(bendX, bendY);
            ctx.lineTo(nextX, nextY);
            ctx.stroke();
            ctx.setLineDash([]); // Reset dash pattern
            
            // Calculate chord length
            const chordLength = calculateChordLength(innerRadius, bend.angle);
            
            // Calculate midpoint for chord length label
            const midX = (bendX + nextX) / 2;
            const midY = (bendY + nextY) / 2;
            
            // Calculate angle for text rotation
            const textAngle = Math.atan2(nextY - bendY, nextX - bendX);
            
            // Draw chord length label
            ctx.save();
            ctx.translate(midX, midY);
            ctx.rotate(textAngle);
            ctx.fillStyle = '#FFA000';
            ctx.fillText(`${chordLength.toFixed(1)}mm`, 0, -10);
            ctx.restore();
        }
    }
    
    // Draw legend
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    const legendX = 10;
    let legendY = 10;
    const legendSpacing = 20;
    
    // Outer radius
    ctx.strokeStyle = '#4CAF50';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(legendX, legendY + 8);
    ctx.lineTo(legendX + 30, legendY + 8);
    ctx.stroke();
    ctx.fillStyle = '#000';
    ctx.fillText(`Külső ív (R=${outerRadius.toFixed(1)}mm)`, legendX + 40, legendY);
    
    // Neutral radius
    legendY += legendSpacing;
    ctx.strokeStyle = '#2196F3';
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.moveTo(legendX, legendY + 8);
    ctx.lineTo(legendX + 30, legendY + 8);
    ctx.stroke();
    ctx.fillText(`Neutrális vonal (rn=${neutralRadius.toFixed(1)}mm)`, legendX + 40, legendY);
    
    // Inner radius
    legendY += legendSpacing;
    ctx.strokeStyle = '#f44336';
    ctx.beginPath();
    ctx.moveTo(legendX, legendY + 8);
    ctx.lineTo(legendX + 30, legendY + 8);
    ctx.stroke();
    ctx.fillText(`Belső ív (r=${innerRadius.toFixed(1)}mm)`, legendX + 40, legendY);

    // Start segment
    if (startLength > 0) {
        legendY += legendSpacing;
        ctx.strokeStyle = '#FF9800';
        ctx.beginPath();
        ctx.moveTo(legendX, legendY + 8);
        ctx.lineTo(legendX + 30, legendY + 8);
        ctx.stroke();
        ctx.fillText(`Kezdő szakasz (${startLength.toFixed(1)}mm)`, legendX + 40, legendY);
    }

    // End segment
    if (endLength > 0) {
        legendY += legendSpacing;
        ctx.strokeStyle = '#9C27B0';
        ctx.beginPath();
        ctx.moveTo(legendX, legendY + 8);
        ctx.lineTo(legendX + 30, legendY + 8);
        ctx.stroke();
        ctx.fillText(`Záró szakasz (${endLength.toFixed(1)}mm)`, legendX + 40, legendY);
    }

    // Add bending point marker to legend
    legendY += legendSpacing;
    ctx.fillStyle = '#FF0000';
    ctx.beginPath();
    ctx.arc(legendX + 15, legendY + 8, 5, 0, 2 * Math.PI);
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.stroke();
    ctx.fillStyle = '#000';
    ctx.fillText('Hajlítási pont', legendX + 40, legendY);
}

function toggleRadiusInput() {
    const radiusType = document.querySelector('input[name="radiusType"]:checked').value;
    const innerGroup = document.getElementById('innerRadiusGroup');
    const neutralGroup = document.getElementById('neutralRadiusGroup');
    
    if (radiusType === 'inner') {
        innerGroup.style.display = 'block';
        neutralGroup.style.display = 'none';
        document.getElementById('neutralRadius').value = '';
    } else {
        innerGroup.style.display = 'none';
        neutralGroup.style.display = 'block';
        document.getElementById('innerRadius').value = '';
    }
}

function calculateBending() {
    const thickness = parseFloat(document.getElementById('thickness').value);
    const kFactor = parseFloat(document.getElementById('kFactor').value);
    const segmentCount = parseInt(document.getElementById('segmentCount').value);
    const bendCount = segmentCount + 1;
    const bendAngle = parseFloat(document.getElementById('angle').value);
    const startLength = parseFloat(document.getElementById('startLength').value) || 0;
    const endLength = parseFloat(document.getElementById('endLength').value) || 0;
    
    // Get radius based on selected type
    const radiusType = document.querySelector('input[name="radiusType"]:checked').value;
    let innerRadius, neutralRadius, outerRadius;
    
    if (radiusType === 'inner') {
        innerRadius = parseFloat(document.getElementById('innerRadius').value);
        neutralRadius = innerRadius + (kFactor * thickness);
        outerRadius = innerRadius + thickness;
    } else {
        neutralRadius = parseFloat(document.getElementById('neutralRadius').value);
        innerRadius = neutralRadius - (kFactor * thickness);
        outerRadius = innerRadius + thickness;
    }
    
    // Validate inputs
    if (isNaN(innerRadius) || isNaN(thickness) || isNaN(kFactor) || 
        isNaN(segmentCount) || isNaN(bendAngle) || isNaN(neutralRadius) ||
        isNaN(startLength) || isNaN(endLength)) {
        document.getElementById('result').textContent = 'Kérem adjon meg érvényes számokat!';
        return;
    }
    
    if (innerRadius <= 0 || thickness <= 0 || segmentCount < 1 || kFactor <= 0) {
        document.getElementById('result').textContent = 'Minden értéknek pozitívnak kell lennie!';
        return;
    }
    
    // Calculate total arc lengths
    const neutralArcLength = neutralRadius * (bendAngle * Math.PI / 180);
    const outerArcLength = outerRadius * (bendAngle * Math.PI / 180);
    const innerArcLength = innerRadius * (bendAngle * Math.PI / 180);
    
    // Calculate values
    const anglePerBend = bendAngle / bendCount;
    const lengthPerBend = neutralArcLength / segmentCount;
    
    // Calculate segments and bends
    const bends = [];
    let totalLength = 0;
    
    for (let i = 0; i < bendCount; i++) {
        const bend = {
            number: i + 1,
            angle: anglePerBend,
            length: lengthPerBend,
            centralAngle: 180 - anglePerBend
        };
        bends.push(bend);
        totalLength += lengthPerBend;
    }

    // Calculate total length including straight segments
    const totalWithStraight = neutralArcLength + startLength + endLength;
    
    // Display results
    document.getElementById('result').innerHTML = `
        <p>Belső rádiusz (r): ${innerRadius.toFixed(2)} mm</p>
        <p>Neutrális rádiusz (rn): ${neutralRadius.toFixed(2)} mm</p>
        <p>Külső rádiusz (R): ${outerRadius.toFixed(2)} mm</p>
        <p>Lemezvastagság (t): ${thickness.toFixed(2)} mm</p>
        <p>K-faktor: ${kFactor.toFixed(3)}</p>
        <p>Hajlítási szög: ${bendAngle}°</p>
        <p>Szegmensek száma (n): ${segmentCount}</p>
        <p>Hajlítások száma (n+1): ${bendCount}</p>
        <p>Egy szegmens hossza: ${lengthPerBend.toFixed(2)} mm</p>
        <p>Egy hajlítás szöge: ${anglePerBend.toFixed(2)}°</p>
        <p>Kezdő egyenes hossza: ${startLength.toFixed(2)} mm</p>
        <p>Záró egyenes hossza: ${endLength.toFixed(2)} mm</p>
        <p>Belső ív hossza: ${innerArcLength.toFixed(2)} mm</p>
        <p>Neutrális vonal hossza: ${neutralArcLength.toFixed(2)} mm</p>
        <p>Külső ív hossza: ${outerArcLength.toFixed(2)} mm</p>
        <p>Teljes hossz: ${totalWithStraight.toFixed(2)} mm</p>
    `;
    
    // Display bend details
    const bendsList = bends.map(bend => 
        `<p>Hajlítás ${bend.number}: Szög = ${bend.angle.toFixed(2)}° (központi szög: ${bend.centralAngle.toFixed(2)}°), Szegmenshossz = ${bend.length.toFixed(2)} mm</p>`
    ).join('');
    
    document.getElementById('segments').innerHTML = `
        <p><strong>Hajlítási adatok (${segmentCount} szegmens, ${bendCount} hajlítás):</strong></p>
        ${startLength > 0 ? `<p>Kezdő egyenes szakasz: ${startLength.toFixed(2)} mm</p>` : ''}
        ${bendsList}
        ${endLength > 0 ? `<p>Záró egyenes szakasz: ${endLength.toFixed(2)} mm</p>` : ''}
    `;
    
    // Draw the visualization with all three arcs and bend information
    drawBendingVisualization(outerRadius, neutralRadius, innerRadius, bendAngle, bends, startLength, endLength);
}

function toggleRadiusType() {
    const radiusType = document.querySelector('input[name="radiusType"]:checked').value;
    const innerGroup = document.getElementById('innerRadiusGroup');
    const neutralGroup = document.getElementById('neutralRadiusGroup');
    
    if (radiusType === 'inner') {
        innerGroup.style.display = 'block';
        neutralGroup.style.display = 'none';
        document.getElementById('neutralRadius').value = '';
    } else {
        innerGroup.style.display = 'none';
        neutralGroup.style.display = 'block';
        document.getElementById('innerRadius').value = '';
    }
}

function calculateBends(totalAngle, segmentCount) {
    // Number of bends is one more than the number of segments
    const bendCount = segmentCount + 1;
    // Each bend angle should be the total angle divided by number of bends
    // This ensures the sum of bend angles equals the angle between start and end segments
    const anglePerBend = totalAngle / bendCount;
    let bends = [];
    let sumOfAngles = 0;
    
    for (let i = 1; i <= bendCount; i++) {
        // For the last bend, use the remaining angle to ensure exact total
        const bendAngle = (i === bendCount) ? (totalAngle - sumOfAngles) : anglePerBend;
        const bendNumber = i;
        bends.push({
            angle: bendAngle,
            number: bendNumber,
            length: 0 // Will be calculated later
        });
        sumOfAngles += bendAngle;
    }
    
    return bends;
}

function calculateArcLengths(outerRadius, neutralRadius, innerRadius, totalAngle, bends) {
    const arcLengthOuter = (2 * Math.PI * outerRadius * totalAngle) / 360;
    const arcLengthNeutral = (2 * Math.PI * neutralRadius * totalAngle) / 360;
    const arcLengthInner = (2 * Math.PI * innerRadius * totalAngle) / 360;
    
    // Calculate segment length - divide by number of segments (bends.length - 1)
    const segmentLength = arcLengthNeutral / (bends.length - 1);
    
    // Update bend lengths
    bends.forEach(bend => {
        bend.length = segmentLength;
    });
    
    return {
        outer: arcLengthOuter,
        neutral: arcLengthNeutral,
        inner: arcLengthInner,
        segmentLength: segmentLength
    };
}

function calculateChordLength(radius, angle) {
    // Convert angle from degrees to radians
    const angleRad = angle * Math.PI / 180;
    // Calculate chord length using: 2 * radius * sin(angle/2)
    return 2 * radius * Math.sin(angleRad / 2);
}

function resetCalculator() {
    // Clear all input fields
    document.getElementById('innerRadius').value = '';
    document.getElementById('neutralRadius').value = '';
    document.getElementById('thickness').value = '';
    document.getElementById('kFactor').value = '';
    document.getElementById('segmentCount').value = '';
    document.getElementById('angle').value = '';
    document.getElementById('startLength').value = '';
    document.getElementById('endLength').value = '';
    
    // Reset radius type to inner
    document.querySelector('input[name="radiusType"][value="inner"]').checked = true;
    toggleRadiusInput();
    
    // Clear results
    document.getElementById('result').textContent = '';
    document.getElementById('segments').textContent = '';
    
    // Clear canvas
    const canvas = document.getElementById('arcCanvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw empty coordinate system
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    ctx.strokeStyle = '#ccc';
    ctx.beginPath();
    ctx.moveTo(50, centerY);
    ctx.lineTo(canvas.width - 50, centerY);
    ctx.moveTo(centerX, 50);
    ctx.lineTo(centerX, canvas.height - 50);
    ctx.stroke();
}
