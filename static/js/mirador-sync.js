// mirador-sync.js
const MiradorSync = {
  viewer: null,
  manifestUrl: null,
  currentWindowId: null,
  observer: null,

  initialize(containerId, manifestUrl) {
    console.log('Initializing MiradorSync with:', { containerId, manifestUrl });
    this.manifestUrl = manifestUrl;
    
    this.viewer = Mirador.viewer({
      id: containerId,
      windows: [{
        manifestId: manifestUrl,
        canvasIndex: 0,
      }],
      window: {
        allowClose: false,
        allowMaximize: false,
        defaultSideBarPanel: 'info',
        sideBarOpenByDefault: false,
      },
      workspace: {
        showZoomControls: true,
        type: 'single',
      }
    });

    // Wait a bit for Mirador to fully initialize
    setTimeout(() => {
      const state = this.viewer.store.getState();
      this.currentWindowId = Object.keys(state.windows)[0];
      console.log('Mirador initialized with:', {
        windowId: this.currentWindowId,
        state: state.windows[this.currentWindowId]
      });
    }, 1000);
  },

  async navigateToFolio(folioNumber) {
    if (!this.viewer || !this.manifestUrl || !folioNumber) {
      console.log('Cannot navigate: missing required data', {
        hasViewer: !!this.viewer,
        manifestUrl: this.manifestUrl,
        folioNumber
      });
      return;
    }

    try {
      console.log('Attempting to navigate to folio:', folioNumber);
      const state = this.viewer.store.getState();
      const manifest = state.manifests[this.manifestUrl].json;
      const canvases = manifest.sequences[0].canvases;
      console.log('Found manifest with', canvases.length, 'canvases');
      
      // Try different patterns for matching folio numbers
      const folioPatterns = [
        new RegExp(`f.?${folioNumber}[rv]?`, 'i'),  // f12v, f.12v, f12r
        new RegExp(`${folioNumber}[rv]?`, 'i'),      // 12v, 12r
        new RegExp(`folio.?${folioNumber}`, 'i')     // folio 12, folio.12
      ];

      // Try to find matching canvas
      const canvasIndex = canvases.findIndex(canvas => 
        folioPatterns.some(pattern => {
          const matchesLabel = pattern.test(canvas.label);
          const matchesMetadata = canvas.metadata && 
            canvas.metadata.some(m => pattern.test(m.value));
          
          if (matchesLabel || matchesMetadata) {
            console.log('Found match:', {
              pattern: pattern.toString(),
              label: canvas.label,
              metadata: canvas.metadata
            });
          }
          
          return matchesLabel || matchesMetadata;
        })
      );

      if (canvasIndex !== -1) {
        console.log('Found matching canvas:', {
          index: canvasIndex,
          label: canvases[canvasIndex].label,
          metadata: canvases[canvasIndex].metadata
        });
        
        // Get the window from the state
        const state = this.viewer.store.getState();
        const window = state.windows[this.currentWindowId];
        
        if (window) {
          console.log('Switching to canvas index:', canvasIndex);
          // Try both SET_CANVAS and SET_CANVAS_INDEX
          this.viewer.store.dispatch({
            type: 'SET_CANVAS',
            windowId: this.currentWindowId,
            canvasId: canvases[canvasIndex]['@id']
          });
          
          this.viewer.store.dispatch({
            type: 'SET_CANVAS_INDEX',
            windowId: this.currentWindowId,
            canvasIndex: canvasIndex
          });
        } else {
          console.log('Could not find window:', this.currentWindowId);
        }
      } else {
        console.log('No matching canvas found for folio:', folioNumber);
        console.log('First few canvas labels:', canvases.slice(0, 5).map(c => ({ 
          label: c.label, 
          metadata: c.metadata 
        })));
      }
    } catch (error) {
      console.error('Error navigating to folio:', error);
    }
  },

  setupIntersectionObserver(handleFolioChange) {
    console.log('Setting up Intersection Observer');
    
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const folioElement = entry.target;
        const folioNumber = folioElement.dataset.folioNumber;
        
        if (entry.isIntersecting) {
          console.log('Folio entered viewport:', folioNumber, 'Intersection ratio:', entry.intersectionRatio);
          folioElement.style.backgroundColor = '#f0f9ff';
          handleFolioChange(folioNumber);
        } else {
          folioElement.style.backgroundColor = '';
        }
      });
    }, {
      root: null,
      rootMargin: '-20% 0px -60% 0px',
      threshold: [0, 0.25, 0.5, 0.75, 1]
    });

    // Observe all folio dividers
    const dividers = document.querySelectorAll('.folio-divider');
    console.log('Found folio dividers:', dividers.length);
    
    dividers.forEach(divider => {
      this.observer.observe(divider);
      console.log('Observing divider with folio:', divider.dataset.folioNumber);
    });
  }
};

// Initialize Alpine data
document.addEventListener('alpine:init', () => {
  Alpine.data('miradorViewer', () => ({
    hasKnownFolios: false,
    manifestUrl: null,
    currentFolio: null,
    viewerInitialized: false,

    init() {
      console.log('Initializing Alpine miradorViewer component');
      this.hasKnownFolios = this.$el.dataset.hasKnownFolios === 'true';
      this.manifestUrl = this.$el.dataset.manifestUrl;
      
      console.log('MiradorViewer initialized with:', {
        hasKnownFolios: this.hasKnownFolios,
        manifestUrl: this.manifestUrl
      });
      
      if (this.manifestUrl) {
        this.$nextTick(() => {
          MiradorSync.initialize('mirador-container', this.manifestUrl);
          this.viewerInitialized = true;
          console.log('Mirador viewer initialized');
          
          // Set up the observer after Alpine and Mirador are initialized
          MiradorSync.setupIntersectionObserver((folioNumber) => {
            this.handleFolioChange(folioNumber);
          });
        });
      }
    },

    handleFolioChange(folioNumber) {
      console.log('Handling folio change:', folioNumber);
      if (this.viewerInitialized) {
        MiradorSync.navigateToFolio(folioNumber);
      } else {
        console.log('Viewer not yet initialized');
      }
    }
  }));
});

