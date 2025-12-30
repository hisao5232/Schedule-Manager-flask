document.addEventListener('DOMContentLoaded', () => {
    const addForm = document.querySelector('.add-form');
    const titleInput = document.querySelector('input[name="title"]');

    // 1. 送信した瞬間に中身をクリアして、次の入力に備える
    if (addForm) {
        addForm.addEventListener('submit', () => {
            // 送信のわずか後に中身を空にする（送信前に消すとデータが飛ばないため）
            setTimeout(() => {
                addForm.reset(); 
                titleInput.focus(); // すぐに次のタスクを打てるようにカーソルを合わせる
            }, 10);
        });
    }

    // 2. すべてのボタンに「押し感」を追加する
    const buttons = document.querySelectorAll('button, .btn, .delete-btn');
    
    buttons.forEach(btn => {
        btn.addEventListener('mousedown', () => {
            btn.style.transform = 'scale(0.95)'; // わずかに小さく（沈む感じ）
            btn.style.transition = 'transform 0.1s';
        });

        btn.addEventListener('mouseup', () => {
            btn.style.transform = 'scale(1)'; // 元に戻す
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'scale(1)'; // マウスが外れたら元に戻す
        });

        // スマホ（タッチ）対応
        btn.addEventListener('touchstart', () => {
            btn.style.transform = 'scale(0.95)';
        }, {passive: true});

        btn.addEventListener('touchend', () => {
            btn.style.transform = 'scale(1)';
        }, {passive: true});
    });
});

// 今後、ドラッグ＆ドロップなどの機能を追加する際に使用します
console.log("Schedule Manager Loaded");
