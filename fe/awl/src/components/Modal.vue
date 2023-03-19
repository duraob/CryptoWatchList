<template>
    <div id='add' class="ui modal">
        <i class="close icon" @click="$emit('close')"></i>
        <div class="header">
            <slot name="header">{{ title }}</slot>
        </div>
        <div class="content">
            <div class="ui form">
                <div class="field">
                    <label>Enter Symbols</label>
                    <textarea id="assets"></textarea>
                </div>
            </div>
        </div>
        <div class="actions">
            <div id='acion' class="ui positive right labeled icon button">
                <slot name="action">{{ action }} Symbols</slot>
                <i class="plus icon"></i>
            </div>
        </div>
    </div>
</template>

<script>
  export default {
    name: 'Modal',
    methods: {
      close() {
        this.$emit('close');
      },
    },
    props: {
        title : {
            type: String,
        },
        action : {
            type : String,
        }

    }
  };
</script>