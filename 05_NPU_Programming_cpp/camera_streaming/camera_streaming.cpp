// Copyright (c) 2025 aNoken

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <unistd.h>

int main()
{
    // �J�����L���v�`���[�I�u�W�F�N�g�̍쐬
    cv::VideoCapture cap;
    // �f�t�H���g�J�����i�ʏ��ID:0�j���I�[�v��
    cap.open(0);

    // HTTP�X�g���[�~���O�p�̃r�f�I���C�^�[�I�u�W�F�N�g�̍쐬
    cv::VideoWriter http;
    // �|�[�g8888��HTTP�X�g���[�~���O���J�n
    http.open("httpjpg", 8888);
    // �u���E�U�ŃA�N�Z�X����ۂ�URL: http://<�T�[�o�[��IP>:8888

    // �J��������̉摜���i�[���邽�߂�Mat�I�u�W�F�N�g
    cv::Mat bgr;

    // �������[�v�ŃX�g���[�~���O���p��
    while (1)
    {
        // �J��������1�t���[�����擾
        cap >> bgr;
        // �擾�����t���[����HTTP�X�g���[���ɑ��M
        http << bgr;
        // �t���[�����[�g�����̂���25�~���b�ҋ@
        usleep(25000);
    }

    return 0;
}
