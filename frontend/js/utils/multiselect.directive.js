angular.module('workbench.utils')

	.directive('multiselect' , [function () {
		return {
			restrict: 'E',
			transclude: true,
			scope: {
				'elements': '='
			},
			templateUrl: 'js/utils/multiselect.html',
			link: function(scope, element, attrs) {
				scope.toggled = true;
				scope.toggleList  = function() {
					scope.toggled = !scope.toggled;
				}
			}

		}
	}]);
