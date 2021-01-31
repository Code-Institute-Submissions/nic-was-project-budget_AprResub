$(document).ready(function(){
    let categoryCount = 1
    
    $("#add-category").click(function(){
        categoryCount++


        $("#categories").append(`
        
            <div class="row category" id="${categoryCount}category">
                <div class="input-field col s5 m5">
                    <input name="${categoryCount}category" type="text" 
                        minlength="5" maxlength="50"  class="validate">
                    <label for="${categoryCount}category">Category Name</label>
                </div>
                <div class="input-field col s5 m5">
                    <select name="${categoryCount}category" class="validate">
                        <option value="per unit" selected>per unit</option>
                        <option value="per hour">per hour</option>
                        <option value="per day">per day</option>
                    </select>   
                </div>
                <div class="col s2 m2">
                    <div class="btn red"><i class="fas fa-times"></i>
                    </div>
                </div>
            </div>

        `)
 
        // dropdown
        $(`select`).formSelect()

        $(`#${categoryCount}category .btn`).click(function(){
            $(this).closest(".category").remove()
            
        })
    })


  });



  





