  import { DjangoComponent, registry } from '/static/sfc/component.js'

  export class List extends DjangoComponent {
    connectedCallback () {}

  }
  registry.registerComponent('list', List)