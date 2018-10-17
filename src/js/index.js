import axios from 'axios';
import cytoscape from 'cytoscape';
import popper from 'cytoscape-popper';
import coseBilkent from 'cytoscape-cose-bilkent';

cytoscape.use(popper);
cytoscape.use( coseBilkent );

var cy = window.cy = cytoscape({
  container: document.getElementById('cy'), // container to render in
  zoom: 3,
  // pan: {
  //   x: 0,
  //   y: 0
  // },
  fit: true,
  ransomize: true,
  layout: {
    name: 'grid',
    fit: false,
    animate: true
  },
  style: [
    {
      selector: '.account',
      style: {
        'border-style': 'dashed',
        'label': 'data(label)',
      }
    },
    {
      selector: '.vpc',
      style: {
        'border-color': '#f76700',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.subnet',
      style: {
        'border-style': 'dotted',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.ec2instance',
      style: {
        'background-image': '/static/icons/aws/Compute/Compute_AmazonEC2.svg',
        // 'background-color': 'white',
        'width': 50,
        'height': 50,
        'background-width': 50,
        'background-height': 50,
        'background-fit': 'none',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    }
  ]
});


axios.get('/data').then((response) => {
  var data = {};
  data = response.data;
  cy.add(data);
  console.log(data);
}).catch((error) => {
  console.error(error);
});
