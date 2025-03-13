// static/js/manuscript.js

document.addEventListener('alpine:init', () => {
    Alpine.data('imageGrid', (imagePool) => ({
        tiles: Array(9).fill().map(() => ({
            currentImage: null,
            nextImage: null,
            isTransitioning: false
        })),
        
        imagePool: imagePool,

        init() {
            console.log('Initializing imageGrid');
            console.log('Image pool length:', this.imagePool.length);
            
            // Initialize tiles with random images
            this.tiles = this.tiles.map((_, index) => {
                const randomImage = this.getRandomImage();
                console.log(`Tile ${index} initialized with:`, randomImage);
                return {
                    currentImage: randomImage,
                    nextImage: null,
                    isTransitioning: false
                };
            });

            // Log the initial state
            console.log('Initial tiles state:', this.tiles);

            // Set up rotation intervals for each tile
            this.tiles.forEach((_, index) => {
                this.setupTileInterval(index);
            });
        },

        getRandomImage(excludeImages = []) {
            const availableImages = this.imagePool.filter(img => !excludeImages.includes(img));
            if (availableImages.length === 0) {
                console.log('No available images, using full pool');
                return this.imagePool[Math.floor(Math.random() * this.imagePool.length)];
            }
            const selected = availableImages[Math.floor(Math.random() * availableImages.length)];
            console.log('Selected random image:', selected);
            return selected;
        },

        setupTileInterval(index) {
            const interval = 3000 + Math.random() * 3000;
            console.log(`Setting up interval for tile ${index}: ${interval}ms`);
            
            setInterval(() => {
                console.log(`Updating tile ${index}`);
                const currentlyDisplayedImages = this.tiles
                    .map(tile => tile.currentImage)
                    .filter(img => img !== this.tiles[index].currentImage);

                this.tiles[index].nextImage = this.getRandomImage(currentlyDisplayedImages);
                this.tiles[index].isTransitioning = true;

                setTimeout(() => {
                    this.tiles[index].currentImage = this.tiles[index].nextImage;
                    this.tiles[index].nextImage = null;
                    this.tiles[index].isTransitioning = false;
                    console.log(`Tile ${index} transition complete:`, this.tiles[index].currentImage);
                }, 1000);
            }, interval);
        }
    }));
});
