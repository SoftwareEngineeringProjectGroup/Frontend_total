<template>
  <div
      class="chat-container"
      :class="{ 'codeBox-active': is_codeBox === 1 }"
  >
    <!-- Initiate 组件 -->
    <div class="initiate">
      <InitialMode @codeBoxAppear="codeBoxAppearance" />
    </div>

    <!-- CodeBox 组件 -->
    <div v-if="is_codeBox === 1" class="codeBox">
      <codeBox :code="exampleCode" language="python" />
    </div>
  </div>
</template>



<script setup lang="ts">
import InitialMode from "@/components/Programming_dev_1/InitialMode.vue";
import codeBox from "@/components/Programming_dev_1/codeBox.vue"
import { ref } from "vue";

const is_codeBox = ref(0);

const exampleCode = ref(`
def merge_sort(arr):
    # Base case: if the array has 1 or no elements, it's already sorted
    if len(arr) <= 1:
        return arr

    # Split the array into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    sorted_array = []
    i = j = 0

    # Merge elements from both halves in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            j += 1

    # Add any remaining elements from the left half
    sorted_array.extend(left[i:])

    # Add any remaining elements from the right half
    sorted_array.extend(right[j:])

    return sorted_array

# Example usage
if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]
    print("Original array:", arr)
    sorted_arr = merge_sort(arr)
    print("Sorted array:", sorted_arr)
`);

const codeBoxAppearance = (message) => {
  is_codeBox.value = message.value;
  console.log(message.value);
};
</script>


<style>
.chat-container {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}


/* 仅在 is_codeBox === 1 时生效的样式 */
.codeBox-active .initiate {
  position: absolute;
  left: 20px;
  z-index: 2;
}

.codeBox-active .codeBox {
  position: absolute;
  width: 50vw;
  height: 100vh;
  right: 100px;
  z-index: 1;
}

</style>
