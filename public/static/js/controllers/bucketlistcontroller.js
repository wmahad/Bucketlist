'use strict';


app.controller('BucketListController',
    function BucketListController($rootScope, $scope, $state, $localStorage, $stateParams, BucketListService, toastr) {
        $(document).ready(function() {
            // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
            $('.modal-trigger').leanModal();
        });
        var BlService = BucketListService;

        $scope.username = $localStorage.currentUser;

        //get bucketlist data
        $scope.Bucketlists = BlService.Bucketlists.getAllBuckets();


        $scope.openModal = function(bucketlist_id) {
            $scope.bucketedit = BlService.Bucketlists.getOneBucket({
                id: bucketlist_id
            });
            $('#modal1').openModal();
        };

        //create a new bucketlist
        $scope.createBucketlist = function() {
            var data = {
                name: $scope.newbucket.name
            };
            BlService.Bucketlists.createBucket(data)
                .$promise
                .then(function(response) {
                    console.log(response);
                    $state.go('dashboard', {}, {
                        reload: true
                    });
                    toastr.success('Bucketlist created successfully');
                })
                .catch(function(responseError) {
                    toastr.error('Bucketlist not created');
                });

        };

        //update bucketlist
        $scope.updateBucketlist = function(_id) {
            var data = {
                name: $scope.bucketedit.name,
                // created_by:$cookies.get('id'),
                id: _id
            };
            console.log(data);
            BlService.Bucketlists.updateBucket(data)
                .$promise
                .then(function(response) {
                    $state.go('dashboard', {}, {
                        reload: true
                    });
                    $('#modal1').closeModal();
                    toastr.success('Bucketlist updated successfully');
                })
                .catch(function(responseError) {
                    toastr.error('Bucketlist not updated');
                });

        };

        //delete individual bucketlist
        $scope.deleteBucketlist = function(bucket) {
            bucket.$deleteBucket().then(function() {
                $state.go('dashboard', {}, {
                    reload: true
                });
                toastr.success('Bucketlist deleted successfully');
            });
        };
    }
);



app.controller('BucketListViewController',
    function BucketListViewController($rootScope, $scope, $state, $localStorage, $stateParams, BucketListService, toastr) {
        $(document).ready(function() {
            // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
            $('.modal-trigger').leanModal();
        });

        $scope.username = $localStorage.currentUser;
        $scope.BucketlistItem = BucketListService.Bucketlists.getOneBucket({
            id: $stateParams.id
        });

        $scope.openItemModal = function(bucketlist_id, item_id) {
            var data = {
                bid: bucketlist_id,
                id: item_id
            };
            $scope.itemedit = BucketListService.BucketlistItems.getOneBucketItem(data);
            $('#modal1').openModal();
        };

        $scope.createBucketItem = function(url_params) {
            BucketListService.BucketlistItems.createBucketItem(url_params)
                .$promise
                .then(
                    function(response) {
                        $state.go('viewBucket', {
                            id: url_params.bid
                        }, {
                            reload: true
                        });
                        toastr.success('Item created successfully');
                    })
                .catch(function(responseError) {
                    toastr.error('Item not created');
                });
        };

        $scope.deleteItem = function(url_params) {
            BucketListService.BucketlistItems.deleteBucketItem(url_params)
                .$promise
                .then(
                    function(response) {
                        $state.go('viewBucket', {
                            id: url_params.bid
                        }, {
                            reload: true
                        });
                        toastr.success('Item deleted successfully');
                    }
                );
        };

        $scope.editItem = function(_id, b_id) {
            var data = {
                name: $scope.itemedit.name,
                id: _id,
                bucketlist: b_id,
                bid: b_id
            };
            BucketListService.BucketlistItems.updateBucketItem(data)
                .$promise
                .then(
                    function(response) {
                        $state.go('viewBucket', {
                            id: b_id
                        }, {
                            reload: true
                        });
                        $('#modal1').closeModal();
                        toastr.success('Item updated successfully');
                    }
                );
        };


        $scope.toggleCompleted = function(item, _id, b_id) {
            var data = {
                done: item.done,
                name: item.name,
                id: _id,
                bucketlist: b_id,
                bid: b_id
            };
            BucketListService.BucketlistItems.updateBucketItem(data)
                .$promise
                .then(
                    function(response) {
                        $state.go('viewBucket', {
                            id: b_id
                        }, {
                            reload: true
                        });
                        toastr.success('Item updated successfully');
                    }
                );
        }

    }
);
