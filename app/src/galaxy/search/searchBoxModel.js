import appEvents from '../service/appEvents.js';
import scene from '../store/scene.js'
import clientRuntime from '../runtime/clientRuntime.js';

import SearchResultWindowViewModel from './SearchResultWindowViewModel.js';

export default searchBoxModel();

const searchResultsWindowId = 'search-results';

function fixSearchResults(searchResults){
  var i;
  var boardname;
  for (i = 0; i < Math.min(20, searchResults.length); i++){
    boardname = searchResults[i].name.split("<>")[1];
    if (boardname && boardname.length) {
      searchResults[i].name = boardname;
    }
  }
  return searchResults;
}

function print_res(res){
  var i;
  for (i = 0; i < 10; i++){
    if (res && res.length){
      console.log(res[i].name.split("<>")[1])
    }
  }
}

function searchBoxModel() {
  let api = {
    search: search,
    submit: submit
  };

  return api;

  function search(newText) {
    if (newText && newText[0] === ':') return; // processed in submit

    var searchResults = scene.find(newText);
    searchResults = fixSearchResults(searchResults);
    var searchResultWindowViewModel = new SearchResultWindowViewModel(searchResults);

    if (searchResults.length) {
      appEvents.showNodeListWindow.fire(searchResultWindowViewModel, searchResultsWindowId);
    } else {
      appEvents.hideNodeListWindow.fire(searchResultsWindowId);
    }
  }

  function submit(command) {
    if (!command || command[0] !== ':') return; // We can handle only commands here

    // Yes, this is not secure, I know
    command = 'with (ctx) { ' + command.substr(1) + ' }';
    var dynamicFunction = new Function('ctx', command);
    dynamicFunction(clientRuntime);
  }
}
