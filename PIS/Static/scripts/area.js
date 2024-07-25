// JavaScript para agregar interactividad a las características

const features = document.querySelectorAll('.feature');

features.forEach(feature => {
    feature.addEventListener('mouseover', () => {
        feature.style.backgroundColor = '#f0f0f0';
    });

    feature.addEventListener('mouseout', () => {
        feature.style.backgroundColor = '#fff';
    });
});

