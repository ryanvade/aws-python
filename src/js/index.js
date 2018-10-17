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
    },
    {
      selector: '.internetgateway',
      style: {
        'background-image': '/static/icons/aws/Networking%20&%20Content%20Delivery/NetworkingContentDelivery_AmazonVPC_internetgateway.svg',
        'width': 50,
        'height': 50,
        'background-width': 50,
        'background-height': 50,
        'background-fit': 'none',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.internetedge',
      style: {
        'width': 2,
        'line-color': 'blue'
      }
    },
    {
      selector: '.securitygroup',
      style: {
        'background-image': '/static/icons/aws/Compute/Compute_AmazonVPC_VPNgateway.svg',
        'width': 50,
        'height': 50,
        'background-width': 50,
        'background-height': 50,
        'background-fit': 'none',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.s3bucket',
      style: {
        'background-image': '/static/icons/aws/Storage/Storage_AmazonS3_bucket.svg',
        'width': 50,
        'height': 50,
        'background-width': 50,
        'background-height': 50,
        'background-fit': 'none',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.user',
      style: {
        'background-image': '/static/icons/aws/General/General_user.svg',
        'width': 50,
        'height': 50,
        'background-width': 50,
        'background-height': 50,
        'background-fit': 'none',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.accesskey',
      style: {
        'background-image': '/static/icons/aws/Security%20Identity%20&%20Compliance/SecurityIdentityCompliance_IAM.svg',
        'width': 50,
        'height': 50,
        'background-width': 50,
        'background-height': 50,
        'background-fit': 'none',
        'label': 'data(label)',
        'shape': 'rectangle'
      }
    },
    {
      selector: '.internet',
      style: {
        'background-image': '/static/icons/aws/General/General_Internet.svg',
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
