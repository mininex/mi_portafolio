particlesJS("particles-js", {
  "particles": {
    "number": { "value": 80 },
    "color": { "value": "#00d4ff" },
    "shape": {
      "type": "polygon",
      "polygon": { "nb_sides": 6 }
    },
    "opacity": { "value": 0.5 },
    "size": { "value": 4 },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#00d4ff",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 3,
      "direction": "none",
      "out_mode": "out"
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": { "enable": true, "mode": "grab" },
      "onclick": { "enable": true, "mode": "push" }
    },
    "modes": {
      "grab": { "distance": 200, "line_linked": { "opacity": 1 } },
      "push": { "particles_nb": 4 }
    }
  },
  "retina_detect": true
});
