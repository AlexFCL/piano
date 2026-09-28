const scaleSets = {
    major: {
        title: 'Gammes majeures',
        scales: [
            { label: 'Do majeur', image: 'images/Scales/C-majeur.png' },
            { label: 'Ré♭ majeur', image: 'images/Scales/Db-majeur.png' },
            { label: 'Ré majeur', image: 'images/Scales/D-majeur.png' },
            { label: 'Mi♭ majeur', image: 'images/Scales/Eb-majeur.png' },
            { label: 'Mi majeur', image: 'images/Scales/E-majeur.png' },
            { label: 'Fa majeur', image: 'images/Scales/F-majeur.png' },
            { label: 'Fa♯ majeur', image: 'images/Scales/Fd-majeur.png' },
            { label: 'Sol majeur', image: 'images/Scales/G-majeur.png' },
            { label: 'La♭ majeur', image: 'images/Scales/Ab-majeur.png' },
            { label: 'La majeur', image: 'images/Scales/A-majeur.png' },
            { label: 'Si♭ majeur', image: 'images/Scales/Bb-majeur.png' },
            { label: 'Si majeur', image: 'images/Scales/B-majeur.png' }
        ]
    },
    naturalMinor: {
        title: 'Gammes mineures naturelles',
        scales: [
            { label: 'Do mineur naturel', image: 'images/Scales/C-mineur-naturel.png' },
            { label: 'Do♯ mineur naturel', image: 'images/Scales/Cd-mineur-naturel.png' },
            { label: 'Ré mineur naturel', image: 'images/Scales/D-mineur-naturel.png' },
            { label: 'Mi♭ mineur naturel', image: 'images/Scales/Eb-mineur-naturel.png' },
            { label: 'Mi mineur naturel', image: 'images/Scales/E-mineur-naturel.png' },
            { label: 'Fa mineur naturel', image: 'images/Scales/F-mineur-naturel.png' },
            { label: 'Fa♯ mineur naturel', image: 'images/Scales/Fd-mineur-naturel.png' },
            { label: 'Sol mineur naturel', image: 'images/Scales/G-mineur-naturel.png' },
            { label: 'Sol♯ mineur naturel', image: 'images/Scales/Gd-mineur-naturel.png' },
            { label: 'La mineur naturel', image: 'images/Scales/A-mineur-naturel.png' },
            { label: 'Si♭ mineur naturel', image: 'images/Scales/Bb-mineur-naturel.png' },
            { label: 'Si mineur naturel', image: 'images/Scales/B-mineur-naturel.png' }
        ]
    }
};

const grid = document.getElementById('scale-grid');
const gridTitle = document.getElementById('scale-grid-title');
const tabs = [...document.querySelectorAll('[data-scale-type]')];

function renderScaleSet(type) {
    const set = scaleSets[type];
    if (!set) return;

    gridTitle.textContent = set.title;
    grid.replaceChildren();

    set.scales.forEach((scale) => {
        const card = document.createElement('article');
        card.className = 'scale-card';

        const title = document.createElement('h3');
        title.textContent = scale.label;

        const imageWrap = document.createElement('div');
        imageWrap.className = 'scale-card__image-wrap';

        const image = document.createElement('img');
        image.src = scale.image;
        image.alt = `Clavier de la gamme ${scale.label}`;
        image.loading = 'lazy';
        image.decoding = 'async';

        image.addEventListener('error', () => {
            image.classList.add('is-error');
            const error = document.createElement('p');
            error.className = 'scale-card__error';
            error.textContent = 'Image indisponible';
            imageWrap.appendChild(error);
        }, { once: true });

        imageWrap.appendChild(image);
        card.append(title, imageWrap);
        grid.appendChild(card);
    });
}

tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
        const type = tab.dataset.scaleType;

        tabs.forEach((candidate) => {
            const isActive = candidate === tab;
            candidate.classList.toggle('is-active', isActive);
            candidate.setAttribute('aria-pressed', String(isActive));
        });

        renderScaleSet(type);
    });
});

renderScaleSet('major');
