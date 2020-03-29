import { router, mount } from 'redom';
import InputScreen from './ui/inputScreen.jsx';
import SyncScreen from './ui/syncScreen.jsx';
import NotSupportedScreen from './ui/supportScreen.jsx';


export default class Router {

  static init(parent, id) {
    Router.instance = router(`#${id}`, {
      input: InputScreen,
      sync: SyncScreen,
      notSupported: NotSupportedScreen,
    });
    mount(parent, Router.instance);
  }

  static update(route, data) {
    this.instance.update(route, data);
  }
}
