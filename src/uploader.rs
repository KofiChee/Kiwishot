use imgur;

pub fn upload(id: String, data: &[u8]) -> Result<imgur::UploadInfo, imgur::UploadError> {
    let handle = imgur::Handle::new(id);
    handle.upload(&data)
}
