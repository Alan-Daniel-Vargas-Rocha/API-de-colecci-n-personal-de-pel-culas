const searchInput = document.getElementById('searchInput');
const movieCards = document.querySelectorAll('.movie-card');
const emptyMessage = document.getElementById('emptyMessage');

searchInput.addEventListener('input', () => {
    const searchText = searchInput.value
        .toLowerCase()
        .trim();

    let visibleMovies = 0;

    movieCards.forEach(movieCard => {
        const movieName = movieCard.dataset.name.toLowerCase();

        const matchesSearch = movieName.includes(searchText);

        movieCard.hidden = !matchesSearch;

        if (matchesSearch) {
            visibleMovies++;
        }
    });

    emptyMessage.hidden = visibleMovies !== 0;
});