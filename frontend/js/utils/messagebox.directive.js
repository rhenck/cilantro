angular.module('workbench.utils')

    .directive('messagebox' , ['messenger', function(messenger) {
        return {
            restrict: 'E',
            templateUrl: 'js/utils/messagebox.html',
            scope: {
                isOpen: '@'
            },
            link: function(scope, elem, attrs) {

                const boostrapClassMap = {
                    warning: "alert-warning",
                    error: "alert-danger",
                    success: "alert-success",
                    info: "alert-info",
                    debug: "alert-debug",
                    urgent: "alert-info alert-urgent",
                };
                scope.getClass = (type) => boostrapClassMap[type] || "alert-info";
                scope.messages = messenger.messages;
                scope.hasContent = () => messenger.messages.length > 0;
                scope.getMain = messenger.getMainMessage;
                scope.clearLog = messenger.clear;
            }
        }
    }]);
