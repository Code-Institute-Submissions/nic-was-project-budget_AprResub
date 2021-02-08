

$(document).ready(function(){
    let itemCount = 10

    let options = $("select[name=0budget_item]").html() 


    $("#add-budget_item").click(function(){

        itemCount++

        $("#budget-items").append(`
        
        <div id="budget-items">   
            <!-- at least one item should be entered  -->
            <div class="row budget_item" id="${itemCount}budget_item">
                <div class="input-field col s3 m3">
                    <input name="${itemCount}budget_item" type="text" 
                        minlength="5" maxlength="50"  class="validate" required>
                    <label for="${itemCount}budget_item">Item Name</label>
                </div>
                <div class="input-field col s3 m3">
                    <input name="${itemCount}budget_item" type="text" 
                        minlength="5" maxlength="150"  class="validate" required>
                    <label for="${itemCount}budget_item">Description</label>
                </div>
                <div class="input-field col s2 m2">
                    <input name="${itemCount}budget_item" type="number"  step=".01"
                        minlength="5" maxlength="150"  class="validate" required>
                    <label for="${itemCount}budget_item">Amount</label>
                </div>
                <div class="input-field col s3 m3">
                    <select name="${itemCount}budget_item" class="validate" required>
                        
                    </select>   
                </div>
                <div class="col s1 m1 btn red"><i class="fas fa-times"></i>
                </div>
            </div>
        </div>

        `)

        $(`select[name=${itemCount}budget_item]`).html(options)

        // dropdown
        $(`select`).formSelect()

        $(`#${itemCount}budget_item .btn`).click(function(){
            $(this).closest(".budget_item").remove()
            
        })
    })


  });




  





