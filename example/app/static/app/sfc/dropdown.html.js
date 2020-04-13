  import { DjangoComponent, registry } from '/static/sfc/component.js'

  class DropDown extends DjangoComponent {
    connectedCallback () {
      this.toggleList()
      this.button.addEventListener('click', i => this.toggleList())
    }

    toggleList () {
      this.list.classList.toggle('hidden')
    }
  }

  registry.registerComponent('dropdown', DropDown)