import React from 'react';
import commonPackageTemplate from './commonPackageTempalte.jsx';

export default require('maco').template(python, React);

function python(props) {
  var model = props.model;

  var link = 'https://boardgamegeek.com/boardgame/' + encodeURIComponent(model.name);
  var linkText = model.name;

  return commonPackageTemplate(model, link, linkText);
}
