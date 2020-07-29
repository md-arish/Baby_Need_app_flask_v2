$("document").ready(function()
    {
        function item_list(item_names)
        {   
                $( "#item_list" ).empty();
                $("#item_list").append("<h2>Items List</h2>");
                item_names.forEach(app);
                function app(name) 
                {
                    var x ="<button class=" +"item_button" + ">" + name +"</button><br>";
                    $("#item_list").append(x);
                }
				$("#item_list").append("<br>");
                click_event();
         }
         item_list(names);
         
         
        function click_event()
        {
        $(".item_button").click(function()
           {
               var item_name =this.textContent;
               $(".update").show();
               $(".insert").hide(); 
               $("#name").prop("readonly", true);
               var url = "/select_data?data=" + item_name;
               var xhttp = new XMLHttpRequest();
               xhttp.onreadystatechange = function() 
               {
                   if (this.readyState == 4 && this.status == 200) 
                   {
                       var item = JSON.parse(this.responseText)
                       $("#show_item").show();
                       $("#name").val(item.name);
                       $("#quantity").val(item.quantity);
                       $("#brand").val(item.brand);
                       $("#colour").val(item.colour);
                       $("#price").val(item.price);
                       if (item.status=="Not Bought")
                       {
                           $("#status").val("Not Bought");
                       }
                       else
                       {
                           $("#status").val("Bought");
                       }
                       $("#menu").hide();
                   }
               };
               xhttp.open("GET", url , true);
               xhttp.send();
           });
           }

        
        
        $("#update").click(function()
            {
                var upname =$("#name").val();
                var upqty =$("#quantity").val();
                var upbrand =$("#brand").val();
                var upcolour =$("#colour").val();
                var upprice =$("#price").val();
                var upstatus =$("#status").val();
                var up_data ={"name":upname,"quantity":upqty,"brand":upbrand,"colour":upcolour,"price":upprice,"status":upstatus};
                $.ajax(
                    {
                        url:"/update",
                        type:"POST",
                        data:up_data,
                        success: function()
                        {
                            $("#show_item").hide();
                            $("#menu").show();
                            $("#message_update").fadeIn(1000,function()
                            {
                                $("#message_update").fadeOut(3000);
                            });
                        }
                    });
            });
            
        $("#delete").click(function()
            {
                var del_name =$("#name").val();
                var url = "/delete?data="+del_name;
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() 
                {
                    if (this.readyState == 4 && this.status == 200) 
                    {
                        $("#show_item").hide();
                        $("#menu").show();
                        
                        for( var i = 0; i < names.length; i++)
                        { 
                            if ( names[i] === del_name) 
                            { 
                                names.splice(i, 1); 
                            }
                        }
                        item_list(names);
                        $("#message_delete").fadeIn(1000,function()
                           {
                               $("#message_delete").fadeOut(3000);
                           });
                    }
                }
                xhttp.open("GET", url , true);
                xhttp.send();
            });
                    
                    
        $("#insert_option").click(function()
            {
                $("#menu").hide();
                $("#show_item").show();
                $(".update").hide();
                $(".insert").show();
                $(".text_box").val("");
                $("#name").prop("readonly", false);
            });     


        $("#insert").click(function()
            {
                var push_name =$("#name").val();
                var in_data ={"name":$("#name").val(),"quantity":$("#quantity").val(),"brand":$("#brand").val(),"colour":$("#colour").val(),"price":$("#price").val()};
                $.ajax(
                {
                    url:"/insert",
                    type:"POST",
                    data:in_data,
                    success: function()
                    {
                        $("#show_item").hide();
                        $("#menu").show();
                        names.push(push_name);
                        item_list(names);
                        $("#message_insert").fadeIn(1000,function()
                           {
                               $("#message_insert").fadeOut(3000);
                           });
                    }
                });    
            
            }); 
            
            
        $("#items_bought").click(function()
            {
            var url ="/display_bought";
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() 
                {
                    if(this.readyState == 4 && this.status == 200) 
                    {
                        var items = JSON.parse(this.responseText);
                        item_list(items.names);
                    }
                }    
               
            xhttp.open("GET", url , true);
            xhttp.send();    
            });    

        $("#items_unbought").click(function()
            {
            var url ="/display_unbought";
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() 
                {
                    if(this.readyState == 4 && this.status == 200) 
                    {
                        var items = JSON.parse(this.responseText);
                        item_list(items.names);
                    }
                }    
               
            xhttp.open("GET", url , true);
            xhttp.send();    
            });    
        $("#all_items").click(function()
            {
                item_list(names);
            });
    });    