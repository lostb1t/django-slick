

var slick = angular.module('slick', ['ngResource', 'ngSanitize', 'ui.router', 'schemaForm', 'ui.slimscroll'])
    .run(function($http, $rootScope, $state, $stateParams, Api) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;

        var response = Api.Settings.get();
        response.$promise.then(function(data) {
            $rootScope.settings = data;
        });
    });

// TODO limit methods for endpoints
slick.factory("Api", function($resource) {
    return {
        Settings: $resource("/admin/api/settings/"),
        Models:  $resource("/admin/api/:app_label/:model/:pk/", { app_label: '@_app_label', model: '@_model', pk: '@_pk'}, { 
            schema: {
                method: 'GET',
                isArray: false,
                url: '/admin/api/:app_label/:model/schema/',
            },
            form: {
                method: 'GET',
                isArray: true,
                url: '/admin/api/:app_label/:model/form/',
            },
        }),
        Apps: $resource("/admin/api/app/:app_label/", { app_label: '@_app_label'})
    };

});

slick.config(function ($stateProvider, $urlRouterProvider, $resourceProvider) {
    $urlRouterProvider.otherwise('/');

    // TODO base on django setting
    $resourceProvider.defaults.stripTrailingSlashes = false;

    var template_base_path = '/static/slick/templates/';

    $stateProvider
      .state('objects', {
        abstract: true,
        url: '/:app_label/:model',
        templateUrl: template_base_path + 'partials/objects.html',
      })
      .state('objects.list', {
        url: '',
        parent: 'objects',
        views: {
            '': {
                templateUrl: template_base_path + 'partials/list.html',
                controller: 'ListViewCtrl'
            }  
        }
      })
      .state('objects.list.detail', {
        parent: 'objects.list',
        url: '/:pk',
        /*
        resolve: {
            formData: function($stateParams, Api) {
                return Api.Models.get({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk});
            },
            formFields: function($stateParams, ModelResource) {
                return Api.Models.schema({ app_label: $stateParams.app_label, model: $stateParams.model});
            },
        },
        */
        views: {
            'detail@objects.list': {
                templateUrl: template_base_path + 'partials/update_form.html',
                controller: 'UpdateViewCtrl'
            }
        }
      });

 });


slick.controller('ListViewCtrl', function($scope, $rootScope, $state, $stateParams, Api) {
    console.log("ListViewCtrl called");

    // Load apps
    Api.Apps.get({ app_label: $stateParams.app_label}, function(data) {
        $scope.app = data;
        
        angular.forEach(data['models'], function(model, key) {
            if (angular.equals(model.name, $stateParams.model)) {
                $scope.model = model;
            }
        });
    })

    Api.Models.query({ app_label: $stateParams.app_label, model: $stateParams.model}, function(data) {
        $scope.objects = data;
    })
    /*
    $scope.DetailView = function(app_label, model, id) {
        $state.go('objects.list.detail', {pk: id});
    }
    */
});


slick.controller('FormController', function($scope, $stateParams, $sce, Api) {
    console.log("FormController called");
    
    /*
    var response = Api.Models.update_form({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk});
    response.$promise.then(function(data) {
        $scope.form = $sce.trustAsHtml(data.form);
    });
    */

    var response = Api.Models.get({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk});
    response.$promise.then(function(data) {
        $scope.model = data;
    });

    var response = Api.Models.schema({ app_label: $stateParams.app_label, model: $stateParams.model});
    response.$promise.then(function(data) {
       $scope.schema = data;
    });

    var response = Api.Models.form({ app_label: $stateParams.app_label, model: $stateParams.model});
    response.$promise.then(function(data) {
        var form = data;
        form.push({
          type: "submit",
          title: "Save"
        });
        $scope.form = form;
    });

    $scope.onSubmit = function(form) {
        // First we broadcast an event so all fields validate themselves
        $scope.$broadcast('schemaFormValidate');
        console.log("called");
        // Then we check if the form is valid
        if (form.$valid) {
            //console.log($scope.model);
            $scope.model.$save();
            //Api.Models.$save({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk}, $scope.model);
          // ... do whatever you need to do with your data.
        }
    };

});


slick.controller('UpdateViewCtrl', function($scope, $stateParams, $sce, Api) {
    console.log("UpdateViewCtrl called");
    //$scope.formData = formData;
    //$scope.formFields = formFields;



    /*
    var response = ModelResource.schema({ app_label: $stateParams.app_label, model: $stateParams.model});
    response.$promise.then(function(data) {
        //$scope.formData = {};
        $scope.formFields = data;
    });

    
    var response = ModelResource.get({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk});
    response.$promise.then(function(data) {
        $scope.formData = data;
    });
    */

});

slick.controller("sidebar", function ($scope, $stateParams, Api) {
    console.log("sidebar called");

    Api.Apps.query(function(data) {
        //console.log(data);
        $scope.apps = data;
    })
});

