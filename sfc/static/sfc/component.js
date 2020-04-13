var DjangoComponent = /** @class */ (function () {
  function DjangoComponent (cmp) {
    var _this = this
    cmp.querySelectorAll('[data-ref]').forEach(function (i) {
      // @ts-ignore
      _this[i.getAttribute('data-ref')] = i
    })
    this.connectedCallback()
  }

  DjangoComponent.prototype.connectedCallback = function () {
    throw 'Components must implement connectedCallback()'
  }
  return DjangoComponent
}())
export { DjangoComponent }
var Record = /** @class */ (function () {
  function Record (cmp, instances) {
    this.cmp = cmp
    this.instances = instances
  }

  return Record
}())
var Registry = /** @class */ (function () {
  function Registry () {
    this.components = {}
    Registry.instance = this
  }

  Registry.new = function () {
    return Registry.instance || new Registry()
  }
  Registry.prototype.registerComponent = function (selector, component) {
    var _this = this
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('[data-cmp=' + selector + ']').forEach(function (x) {
        var record = _this.components[selector]
        if (!record) {
          record = _this.components[selector] = new Record(component, [])
        }
        record.instances.push(new component(x))
      })
    })
  }
  return Registry
}())
export var registry = Registry.new()
